import difflib

target = "Ankinapally".lower()
cand1 = "Akinepalli".lower() # Intended
cand2 = "Kurnapally".lower() # Matched

ratio1 = difflib.SequenceMatcher(None, target, cand1).ratio()
print(f"Target vs {cand1}: {ratio1}")

ratio2 = difflib.SequenceMatcher(None, target, cand2).ratio()
print(f"Target vs {cand2}: {ratio2}")

matches = difflib.get_close_matches(target, [cand1, cand2], n=3, cutoff=0.5)
print(f"Matches: {matches}")
