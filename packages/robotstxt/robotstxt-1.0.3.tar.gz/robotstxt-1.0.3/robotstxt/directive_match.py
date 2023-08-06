import urllib.parse

# Break a pattern into elements and clean up
def pattern_to_elements(pattern, debug=False):
    # replace multiple * with a single * as they are equivalent

    pattern = urllib.parse.unquote(pattern)
    while '**' in pattern:
        pattern = pattern.replace('**', '*')
    if debug: print("The pattern after replacement of multiple * : " + pattern)

    # Remove any trailing * as matches are broad by default
    if pattern[-1:] == '*':
        pattern = pattern[:-1]
    if debug: print("The pattern after replacement of trailing * : " + pattern)

    # Remove any trailing *$ as matches are broad by default
    if pattern[-2:] == '*$':
        pattern = pattern[:-2]
    if debug: print("The pattern after replacement of trailing *$ : " + pattern)

    # Split the pattern into chunks
    pattern_elements = pattern.split('*')

    if debug: print(f'Pattern elements: {pattern_elements}')

    return pattern_elements

# Test if a URL path matches a pattern
def pattern_match(pattern, path, debug=False):

    path = urllib.parse.unquote(path)

    pattern_elements = pattern_to_elements(pattern, debug=debug)

    # A position marker to update as we move through the path
    position = 0

    # Match the pattern elements against the path
    for x, pattern_element in enumerate(pattern_elements):

        # Set a boolean if the pattern element is the last one and ends with an end of line character ($), and remove the $ character.
        end_match = False
        if x == len(pattern_elements) - 1:
            if pattern_element[-1:] == "$":
                if debug: print('Last pattern element contains end of line')
                end_match = True
                pattern_element = pattern_element[:-1]

        # First match not using a wildcard must be found at the start of the path.
        if x==0 and pattern_element[:1] != '*':
            if debug: print('searching for first element')
            if not path.startswith(pattern_element):
                return False
            else:
                # Update the position to end of the match.
                position = len(pattern_element)
                if end_match:
                    if len(path) > position:
                        return False

        # Otherwise matches can be anywhere from the current position
        else:
            if debug: print('---------------------------')
            if debug: print(f'Searching for {pattern_element} from position {position}')
            find_position = path.find(pattern_element, position)
            if debug: print(f'X: {x}')

            if find_position>-1:
                if debug: print(f'Found {pattern_element} at position {find_position}')
                position = find_position + len(pattern_element)
                if debug: print(f'New position is {position}')
                if end_match:
                    if len(path) > position:
                        if debug: print('there are more characters in the path so the match has failed')
                        return False
            else:
                if debug:
                    print(f'Did not find {pattern_element}')
                    print('#####################################################')
                return False
    if debug: print('#####################################################')
    return True

