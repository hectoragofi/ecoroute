def capitalize_input():
    # Take two inputs from the user
    input1 = input("Enter the first input: ")
    input2 = input("Enter the second input: ")

    # Capitalize the first letter of each word using title() method
    formatted_input1 = input1.title()
    formatted_input2 = input2.title()

    # Print the formatted inputs
    print("Formatted Input 1:", formatted_input1)
    print("Formatted Input 2:", formatted_input2)

# Call the function
capitalize_input()
