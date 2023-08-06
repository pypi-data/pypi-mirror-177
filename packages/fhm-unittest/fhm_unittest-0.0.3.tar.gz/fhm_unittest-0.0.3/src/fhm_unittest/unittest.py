from fuzzywuzzy import fuzz


def output_test(returned_output, expected_output):
  score = fuzz.WRatio(returned_output, expected_output)
  if score == 100:
    print("Perfect! Your output is correct.")
  elif score > 95:
    print(f'You have a {score}% match with the expected output! Try chaging a bit to make it a 100% match.')
  else:
    print(f"You have a {score}% match with the expected output! Please try again.")
