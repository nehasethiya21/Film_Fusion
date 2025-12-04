import os
from cerebras.cloud.sdk import Cerebras

client = Cerebras(
    # This is the default and can be omitted
    api_key="csk-hykry3ed95rx2xjk36p65mhvecm8n4hmd68kj36xmv2nxdt9"
)
def Recomend(py_code):
  stream = client.chat.completions.create(
      messages=[
          {
              "role": "system",
              "content": 'You are an avid Movie expert. You are asked to name the 6 most similar movies to a specific Title. NO INTROS NO OUTROS, seperate Movie names with / '
          },
          {
              "role":"user",
              "content":py_code
          }
      ],
      model="qwen-3-32b",
      stream=True,
      max_completion_tokens=4096,
      temperature=0.2,
      top_p=1
  )

  ALL=""
  for chunk in stream:
    ALL+=chunk.choices[0].delta.content or ""

  return sorted(ALL.split("</think>")[1].split('\n'))[-1].split('/')

#print(Recomend(input("->")))