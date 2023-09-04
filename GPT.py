#ChatGPT3.5

def askGPT(openai, messages):
  chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
  reply = chat.choices[0].message.content
  return reply