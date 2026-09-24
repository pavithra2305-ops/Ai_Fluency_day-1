# Create a very large HTML page for Failure 3

with open("big.html", "w", encoding="utf-8") as file:

    file.write("<html><body>\n")
    file.write("<h1>Student List</h1>\n")

    for i in range(1, 3001):
        file.write(
            f"<p>Student {i}: "
            f"Name=Student_{i}, "
            f"Department=AI and Data Science, "
            f"Year=3, "
            f"Status=Active</p>\n"
        )

    file.write("</body></html>\n")

print("big.html created successfully.")