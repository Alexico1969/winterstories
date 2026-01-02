import os, glob
import pandas as pd
from tqdm import tqdm
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "openai-community/roberta-base-openai-detector"  # GPT-2 output detector :contentReference[oaicite:1]{index=1}

def chunk_by_tokens(text, tokenizer, max_tokens=450):
    # max_tokens kept < 512 to leave room for special tokens
    ids = tokenizer.encode(text, add_special_tokens=False)
    for i in range(0, len(ids), max_tokens):
        yield tokenizer.decode(ids[i:i+max_tokens], skip_special_tokens=True)

def ai_prob_for_text(text, tokenizer, model, device):
    text = " ".join(text.split())
    if not text:
        return None

    probs = []
    weights = []

    for chunk in chunk_by_tokens(text, tokenizer):
        inputs = tokenizer(chunk, return_tensors="pt", truncation=True, max_length=512).to(device)
        with torch.no_grad():
            logits = model(**inputs).logits[0]
            p = torch.softmax(logits, dim=-1).cpu().tolist()

        # Model labels are typically ["Real", "Fake"] where Fake ~= AI-generated :contentReference[oaicite:2]{index=2}
        id2label = model.config.id2label
        # Find which index corresponds to "Fake"
        fake_idx = None
        for k, v in id2label.items():
            if str(v).lower() == "fake":
                fake_idx = int(k)
                break
        if fake_idx is None:
            # fallback: assume label 1 is "Fake"
            fake_idx = 1 if len(p) > 1 else 0

        probs.append(p[fake_idx])
        weights.append(len(chunk.split()))

    if not probs:
        return None
    # Weighted average by chunk word count
    return sum(pi*wi for pi, wi in zip(probs, weights)) / sum(weights)

def main(folder):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME).to(device)
    model.eval()

    rows = []
    for path in tqdm(sorted(glob.glob(os.path.join(folder, "*.txt")))):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        prob = ai_prob_for_text(text, tokenizer, model, device)
        words = len(text.split())
        rows.append({
            "file": os.path.basename(path),
            "words": words,
            "ai_probability_0_to_1": None if prob is None else round(prob, 4)
        })

    df = pd.DataFrame(rows).sort_values(by="ai_probability_0_to_1", ascending=False, na_position="last")
    out = os.path.join(folder, "ai_detection_report.csv")
    df.to_csv(out, index=False)
    print(f"\nSaved: {out}\nTop 10 most-suspicious:")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main(r"''' + $FOLDER + '''")
