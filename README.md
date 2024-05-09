Setup steps
1) Clone this repository on your local machine
2) Go inside the Fatmug directory
3) Install django using `pip install django` (Make sure python is installed on your system)
4) We are using rest_framework, so use `pip install djangorestframework` to use it.
5) For token based authentication, we have to create a user using `python manage.py createsuperuser` to generate a token.
6) After creating a user, use the command `python manage.py drf_create_token <your_username>`
   your result will be like this `Generated token 893f38d0382f9bfaaf69784cfbd5bb31110d1856 for user <username>`
7) Now, run the server using `python manage.py runserver`

Now you api is live on localhost 8000

I have used POSTMAN to test the endpoints of the api.

Because, of encapsulating the urls by token based authentication, we have to add the token everytime in the request in its header.
We have to add it like this: `Authorization: Token 893f38d0382f9bfaaf69784cfbd5bb31110d1856`

Look at the following image:
![Screenshot 2024-05-09 172528](https://github.com/shreyashrpawar/Fatmug/assets/87687490/1fdfaaff-a952-44e6-9da5-eeef2eb0d1f8)

For the post request, you have to enter the url in address bar and select the POST from the dropdown. Enter the data inside Body as shown in image:
![image](https://github.com/shreyashrpawar/Fatmug/assets/87687490/ef9d3324-44c6-4168-ba03-ddc0ae09b22a)

In this way, you can use POSTMAN to check your all the endpoints.
