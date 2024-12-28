# from ollama import Client

# # Initialize the client
# client = Client(host='http://localhost:11434')

# # Define the path to your image
# # image_path = '/home/mahsa/Desktop/download1.jpeg'

# # Define the question you want to ask about the image
# question = f"how i solve my programinig questions? "
# print(question)
# # Call the model with the image and the question
# response = client.chat(model="llava-llama3:latest", messages=[{'role':'user','content':question}])


# # Print the model's response
# print(response['message']['content'])




import ollama
image_path = '/images/download.jpeg'

res = ollama.chat(
    model='llava-llama3:latest',
    messages=[
        {
            'role': 'user',
            'content':'Describe this image in English',
            'image':[image_path]

        }
    ]

)
print(res['message']['content'])

