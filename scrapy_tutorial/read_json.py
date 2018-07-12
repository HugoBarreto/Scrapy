import json
import jsonlines

with open('quotes.json', 'r') as fquotes:
    quotes_json = json.load(fquotes)

with open('quotes.jl', 'r') as fquotes:
    quotes_jl = []
    for line in fquotes:
        quotes_jl.append(json.loads(line))
