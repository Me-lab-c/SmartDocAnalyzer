from transformers import pipeline

# 🔥 Load model once
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def split_text(text, max_words=400):
    words = text.split()
    return [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]


def generate_summary(text):

    chunks = split_text(text)
    summaries = []

    # 🔥 Step 1: summarize ALL chunks
    for chunk in chunks:
        try:
            result = summarizer(
                chunk,
                max_length=120,
                min_length=40,
                do_sample=False
            )
            summaries.append(result[0]['summary_text'])
        except Exception as e:
            print("Error:", e)

    # 🔥 Step 2: combine
    combined = " ".join(summaries)

    # 🔥 Step 3: final summary
    try:
        final = summarizer(
            combined,
            max_length=150,
            min_length=50,
            do_sample=False
        )
        return final[0]['summary_text']
    except:
        return combined