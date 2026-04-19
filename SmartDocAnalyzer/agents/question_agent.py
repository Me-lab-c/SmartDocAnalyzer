import re

def extract_questions(text):
    lines = text.split("\n")
    results = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # ✅ 1. Real questions
        if line.endswith("?"):
            results.append(line)
            continue

        # ✅ 2. Form fields (Name:, Email:, etc.)
        match = re.match(r"^([A-Za-z ]+):\s*(.*)$", line)

        if match:
            label = match.group(1).strip()
            value = match.group(2).strip()

            # 🔥 IMPORTANT CHANGE:
            # Always include — value unna / lekapoina
            if value:
                results.append(f"{label}: {value}")
            else:
                results.append(f"{label}:")
            
            continue

    # If nothing found
    if not results:
        return ["No questions or form fields found."]

    return results              

def extract_questions(text):
    lines = text.split("\n")
    results = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # 🔹 1. QUESTIONS (ending with ?)
        if line.endswith("?"):
            results.append(line)
            continue

        # 🔹 2. QUESTIONS (starting words)
        if re.match(r"^(What|Why|How|When|Where|Explain|Define)\b", line, re.IGNORECASE):
            results.append(line)
            continue

        # 🔹 3. FORM FIELDS (Name:, Email:, etc.)
        match = re.match(r"^([A-Za-z][A-Za-z ]{0,30}):\s*(.*)$", line)

        if match:
            label = match.group(1).strip()
            value = match.group(2).strip()

            # 🔥 INCLUDE BOTH CASES
            if value:
                results.append(f"{label}: {value}")
            else:
                results.append(f"{label}:")

            continue

        # 🔹 4. NUMBERED QUESTIONS (1. What is...)
        if re.match(r"^\d+\.\s+", line):
            results.append(line)
            continue

    # 🔥 If nothing found
    if not results:
        return ["No questions or form fields found."]

    return results