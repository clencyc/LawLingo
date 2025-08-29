import google.generativeai as genai
genai.configure(api_key="AIzaSyBsYjsR2A-iL1uDmTmcuu4mOagnqNZpyxs")
print([m.name for m in genai.list_models()])