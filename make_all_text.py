# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="model-identifier",
  messages=[
    {"role": "system", "content": """
     Your task is to remove all references to the fact that this is an image , here  example:
     Given  text: This is an image of a house with a modern design, featuring large windows and a swimming pool. The house has a flat roof with wooden beams, and the surrounding area includes green foliage and a paved walkway leading to a door.
     Your output: House with a modern design, featuring large windows and a swimming pool. The house has a flat roof with wooden beams, and the surrounding area includes green foliage and a paved walkway leading to a door.
     Can you remove any additional details that arent essential to the core description? For example, can we simplify "The house has a flat roof with wooden beams" to just "The roof is flat with wooden beams"? Also, can you remove any mention of the surrounding area being green and having a paved walkway?
     """},
    {"role": "user", "content": """ The image depicts a cozy and rustic interior of a wooden cabin, with stone floors and stone walls. There are various pieces of furniture, including a couch and a bookshelf, as well as some decorative items like vases and a pot.  """}
  ],
  temperature=0.9,
)

print(completion.choices[0].message)