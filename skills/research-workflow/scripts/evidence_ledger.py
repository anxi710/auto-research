"""Read-only structural checks for optional claim/evidence attempt artifacts.

The caller supplies the existing research-root path resolver and hash checker.
No check here decides scientific support, reading depth, or human approval.
"""
import json
import math
import re
from decimal import Decimal, InvalidOperation


def text(value):
    return isinstance(value, str) and bool(value.strip())


def texts(value):
    return isinstance(value, list) and all(text(item) for item in value)


def identifier(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", value))


def digest(value):
    return isinstance(value, str) and bool(re.fullmatch(r"[a-fA-F0-9]{64}", value))


def number(value):
    return type(value) is int or (type(value) is Decimal and value.is_finite())


def strict_equal(left, right):
    """Compare JSON values without treating booleans as numbers."""
    if type(left) is not type(right):
        return number(left) and number(right) and left == right
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(strict_equal(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(strict_equal(a, b) for a, b in zip(left, right))
    return left == right


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key.")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Non-finite JSON number.")


def finite_decimal(value):
    # Preserve the earlier range guard; comparisons never use its rounded float.
    if not math.isfinite(float(value)):
        raise ValueError("JSON decimal exceeds finite binary64 conversion range.")
    try:
        return Decimal(value)
    except InvalidOperation as error:
        raise ValueError("JSON decimal exponent is outside the supported range.") from error


def pointer_tokens(pointer):
    """Decode RFC 6901 tokens without accepting malformed escape sequences."""
    if not isinstance(pointer, str) or not pointer.startswith("/"):
        raise ValueError("Expected an absolute JSON Pointer.")
    parts = pointer[1:].split("/")
    if any(re.search(r"~(?![01])", part) for part in parts):
        raise ValueError("Invalid JSON Pointer escape.")
    return [part.replace("~1", "/").replace("~0", "~") for part in parts]


def resolve_pointer(value, tokens):
    for token in tokens:
        if isinstance(value, dict):
            if token not in value:
                raise ValueError("Unknown JSON Pointer member.")
            value = value[token]
        elif isinstance(value, list):
            if not re.fullmatch(r"0|[1-9][0-9]*", token):
                raise ValueError("Invalid JSON Pointer array index.")
            index = int(token)
            if index >= len(value):
                raise ValueError("JSON Pointer array index is out of range.")
            value = value[index]
        else:
            raise ValueError("JSON Pointer traverses a scalar.")
    return value


class LedgerValidator:
    def __init__(self, lint):
        self.lint = lint

    def issue(self, code, source, message):
        self.lint.issue(code, source, message)

    def fields(self, value, required, source, label, optional=None):
        optional = optional or {}
        if not isinstance(value, dict):
            self.issue("SCHEMA", source, f"{label} must be an object.")
            return False
        valid = True
        for key, check in required.items():
            if key not in value or not check(value[key]):
                self.issue("SCHEMA", source, f"Invalid or missing {label}.{key}.")
                valid = False
        for key in value:
            if key not in required and key not in optional:
                self.issue("SCHEMA", source, f"Unknown {label}.{key}; review verdicts belong in review records.")
                valid = False
            elif key in optional and not optional[key](value[key]):
                self.issue("SCHEMA", source, f"Invalid {label}.{key}.")
                valid = False
        return valid

    def read(self, path, source, structured=False):
        try:
            content = (self.lint.root / path).read_bytes().decode("utf-8")
        except (OSError, UnicodeError):
            self.issue("READ", source, f"Cannot read UTF-8 evidence: {path}.")
            return None
        if not structured:
            return content
        try:
            return json.loads(content, object_pairs_hook=unique_object,
                              parse_constant=reject_constant, parse_float=finite_decimal)
        except (ValueError, RecursionError):
            self.issue("SCHEMA", source, f"Evidence must contain valid JSON with unique keys and finite numbers: {path}.")
            return None

    def referenced(self, entry, source, structured=False):
        path = self.lint.reference(entry["artifact"], source, entry["sha256"])
        return self.read(path, source, structured) if path is not None else None

    def validate(self, path, source, result):
        ledger = self.read(path, source, structured=True)
        if not self.fields(ledger, {"schema_version": lambda v: v == "1", "task_id": identifier,
                                    "attempt_id": identifier, "claims": lambda v: isinstance(v, list) and bool(v)},
                           source, "evidence_ledger"):
            return None
        if any(ledger[key] != result[key] for key in ("task_id", "attempt_id")):
            self.issue("BINDING", source, "Evidence ledger identity does not match its result.")
        claim_ids, evidence_ids = set(), set()
        for index, claim in enumerate(ledger["claims"]):
            label = f"claims[{index}]"
            if not self.fields(claim, {"claim_id": identifier, "text": text, "location": lambda v: isinstance(v, dict),
                                       "evidence": lambda v: isinstance(v, list) and bool(v),
                                       "verification_request": lambda v: isinstance(v, dict)}, source, label):
                continue
            if claim["claim_id"] in claim_ids:
                self.issue("DUPLICATE_ID", source, f"Duplicate claim_id: {claim['claim_id']}.")
            claim_ids.add(claim["claim_id"])
            self.fields(claim["verification_request"], {"question": text, "limitations": texts}, source,
                        label + ".verification_request")
            location = claim["location"]
            if self.fields(location, {"artifact": text, "sha256": digest, "exact_quote": text}, source, label + ".location"):
                if location["exact_quote"] != claim["text"]:
                    self.issue("BINDING", source, f"{label}.location.exact_quote must equal the claim text.")
                manuscript = self.referenced(location, source)
                if manuscript is not None:
                    quote = location["exact_quote"]
                    first = manuscript.find(quote)
                    if first < 0 or manuscript.find(quote, first + 1) >= 0:
                        self.issue("BINDING", source, f"{label} must occur exactly once in its fixed manuscript, including overlapping matches.")
            for offset, evidence in enumerate(claim["evidence"]):
                evidence_label = label + f".evidence[{offset}]"
                if isinstance(evidence, dict) and identifier(evidence.get("evidence_id")):
                    if evidence["evidence_id"] in evidence_ids:
                        self.issue("DUPLICATE_ID", source, f"Duplicate evidence_id: {evidence['evidence_id']}.")
                    evidence_ids.add(evidence["evidence_id"])
                self.evidence(evidence, source, evidence_label)
        return ledger

    def evidence(self, value, source, label):
        common = {"evidence_id": identifier, "kind": lambda v: v in ("experiment", "literature"),
                  "availability": lambda v: v in ("available", "missing", "inaccessible", "version_uncertain"),
                  "scope": text, "limitations": texts}
        if not isinstance(value, dict) or value.get("kind") not in ("experiment", "literature"):
            self.issue("SCHEMA", source, f"{label} must be experiment or literature evidence.")
            return
        if value["kind"] == "experiment":
            fields = dict(common, artifact=text, sha256=digest, locator=lambda v: isinstance(v, dict), value=number,
                          unit=text, context=lambda v: isinstance(v, dict), baseline_locator=text, baseline_value=number)
            if not self.fields(value, fields, source, label):
                return
            if value["availability"] != "available":
                self.issue("SCHEMA", source, f"{label}: experiment evidence must be available.")
            locator_valid = self.fields(value["locator"], {"type": lambda v: v == "json_pointer", "value": text},
                                        source, label + ".locator")
            context_valid = self.fields(value["context"], {"dataset": text, "split": text, "method": text,
                                                           "baseline": text, "conditions": lambda v: isinstance(v, dict)},
                                        source, label + ".context")
            if not locator_valid or not context_valid:
                return
            data = self.referenced(value, source, structured=True)
            self.measurement(data, value["locator"]["value"], value, source, label, baseline=False)
            self.measurement(data, value["baseline_locator"], value, source, label, baseline=True)
        else:
            fields = dict(common, artifact=lambda v: v is None or text(v), sha256=lambda v: v is None or digest(v),
                          source=lambda v: isinstance(v, dict), locator=lambda v: isinstance(v, dict))
            if not self.fields(value, fields, source, label, {"reason": text}):
                return
            self.literature(value, source, label)

    def measurement(self, data, pointer, evidence, source, label, baseline):
        try:
            tokens = pointer_tokens(pointer)
            if tokens[-1] != "value":
                raise ValueError("Numeric pointers must end at /value.")
            parent = resolve_pointer(data, tokens[:-1])
            if not isinstance(parent, dict):
                raise ValueError("Numeric pointer needs a measurement object.")
            context = evidence["context"]
            expected = {key: context[key] for key in ("dataset", "split", "conditions")}
            expected.update(value=evidence["baseline_value"] if baseline else evidence["value"],
                            unit=evidence["unit"], method=context["baseline"] if baseline else context["method"])
            if not baseline:
                expected["baseline"] = context["baseline"]
            if not number(parent.get("value")) or any(key not in parent or not strict_equal(parent[key], value)
                                                     for key, value in expected.items()):
                raise ValueError("Measurement value, unit, dataset, split, method, baseline, or conditions differ.")
        except (ValueError, RecursionError):
            name = "baseline" if baseline else "method"
            self.issue("BINDING", source, f"{label}: {name} JSON Pointer must bind the exact normalized measurement and context: {pointer!r}.")

    def literature(self, value, source, label):
        retained = value["source"]
        valid = self.fields(retained, {"version": text, "identifier": text,
                                      "reading_depth": lambda v: v in ("metadata", "abstract", "excerpt", "full_text"),
                                      "access_limitations": texts,
                                      "content_kind": lambda v: v in ("none", "metadata", "excerpt", "full_text")}, source, label + ".source")
        valid = self.fields(value["locator"], {"type": lambda v: v in ("page", "section", "quote"), "value": text},
                            source, label + ".locator") and valid
        if not valid:
            return
        if (value["artifact"] is None) != (value["sha256"] is None):
            self.issue("SCHEMA", source, f"{label}: source artifact and SHA256 must both be present or both null.")
            return
        if value["availability"] != "available" and (not text(value.get("reason")) or not retained["access_limitations"]):
            self.issue("SCHEMA", source, f"{label}: unavailable or uncertain sources need a reason and access limitations.")
        if value["artifact"] is None:
            if retained["content_kind"] != "none" or not value["limitations"] or not retained["access_limitations"]:
                self.issue("SCHEMA", source, f"{label}: absent local content needs content_kind none and explicit stability/access limitations.")
            return
        if retained["content_kind"] == "none":
            self.issue("SCHEMA", source, f"{label}: retained source content cannot have content_kind none.")
        if retained["reading_depth"] == "full_text" and retained["content_kind"] != "full_text":
            if not value["limitations"] or not retained["access_limitations"]:
                self.issue("SCHEMA", source, f"{label}: declared full-text reading without retained full text needs explicit stability/access limitations.")
        path = self.lint.reference(value["artifact"], source, value["sha256"])
        if path is not None and value["locator"]["type"] == "quote":
            content = self.read(path, source)
            if content is not None and value["locator"]["value"] not in content:
                self.issue("BINDING", source, f"{label}: source quote does not occur in the fixed local content.")

    def validate_review(self, block, source, result, ledger_path, ledger):
        if not self.fields(block, {"ledger": lambda v: isinstance(v, dict), "assessments": lambda v: isinstance(v, list),
                                   "unreviewed_claim_ids": lambda v: isinstance(v, list) and all(identifier(item) for item in v)},
                           source, "claim_evidence"):
            return
        if self.fields(block["ledger"], {"path": text, "sha256": digest}, source, "claim_evidence.ledger"):
            path = self.lint.reference(block["ledger"]["path"], source, block["ledger"]["sha256"])
            if path != ledger_path or ledger_path is None:
                self.issue("BINDING", source, "Review must reference its result's exact claim/evidence ledger.")
        if ledger is None:
            self.issue("BINDING", source, "Review claim assessments require a valid result ledger.")
            return
        claim_ids = {claim["claim_id"] for claim in ledger["claims"]
                     if isinstance(claim, dict) and identifier(claim.get("claim_id"))}
        covered = list(block["unreviewed_claim_ids"])
        for index, assessment in enumerate(block["assessments"]):
            if self.fields(assessment, {"claim_id": identifier,
                                        "verdict": lambda v: v in ("yes", "partial", "no", "unable_to_assess"),
                                        "scope": text, "reason": text, "gaps": texts, "follow_up": texts},
                           source, f"claim_evidence.assessments[{index}]"):
                covered.append(assessment["claim_id"])
        if len(covered) != len(set(covered)) or set(covered) != claim_ids:
            self.issue("BINDING", source, "Reviewed and explicitly unreviewed claim IDs must partition every ledger claim exactly once.")
