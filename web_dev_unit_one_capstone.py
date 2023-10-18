import re
from html_content import user_string


def check_html_tags(html_string):
    # Define tags and their point values
    tags_points = {
        '<!doctype html>': 5,
        '<html>': 5,
        '<head>': 5,
        '<title>': 5,
        '<body>': 5,
        '<table>': 25,
        '<img>': 10,
        '<p>': 5,
        '<h1>': 5
    }

    total_points = 0
    missing_tags = []

    # Check for each tag and its closing counterpart
    for tag, points in tags_points.items():
        # Special case for DOCTYPE and img as they don't have closing tags
        if tag == '<!doctype html>':
            if tag in html_string:
                total_points += points
            else:
                missing_tags.append(tag)
        elif tag == '<img>':
            # Search for img tag with any attributes
            img_pattern = '<img[^>]*>'
            if re.search(img_pattern, html_string):
                total_points += points
            else:
                missing_tags.append(tag)
        else:
            # Construct regex pattern to account for attributes and spaces
            pattern = re.escape(tag[:-1]) + '[^>]*>' + '(?:.|\\n)*?' + re.escape(tag.replace('<', '</'))
            matches = re.findall(pattern, html_string)

            if matches:
                total_points += points
            else:
                missing_tags.append(tag)

    # Check for at least 3 <p> tags, but only award points up to 15
    p_tags_count = len(re.findall('<p>', html_string))
    if p_tags_count > 0:
        total_points += min(p_tags_count, 3) * tags_points['<p>']
        if p_tags_count < 3:
            missing_tags.append(f'<p> x {3 - p_tags_count}')

    # Check for <ol> or <ul> or <li>
    if not (re.search('<ol>', html_string) or re.search('<ul>', html_string) or re.search('<li>', html_string)):
        missing_tags.append('<ol> or <ul> or <li>')
    else:
        total_points += 15  # Add a suitable point value for <ol> or <ul>

    # Check for subtitle tags (h2 through h6)
    if not re.search('<h[2-6]>.*?</h[2-6]>', html_string):
        missing_tags.append('subtitle (h2-h6)')

    # Display results
    print(f"Total Points: {total_points}")
    if missing_tags:
        print("Missing Tags:")
        for tag in missing_tags:
            print(tag)

# Example usage:
check_html_tags(user_string)
