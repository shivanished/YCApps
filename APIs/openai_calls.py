from openai import OpenAI

# OPENAI_KEY = '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'
client = OpenAI()


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)