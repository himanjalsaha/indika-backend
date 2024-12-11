created a flask backend

intuition was pretty Straight-forward

I'm fairly new to aws and after going through the documentation I was able to spin a s3 bucket and upload files on it

next I had to access it I used boto3 aws sdk for python to create s3 instance and reading from the bucket andiw manipulated it to a dictionary and served response but the link was not pre-signed 

I looked through documentation and found about the pre-signed url method and  created presigned urls

next connected pymongo and stored the response as it isa and it checks if it already exists to prevent duplicates (I used alittleg help of gpt herd I got stuck) 


to to serve byte streaming I didn't write an api as I saw s3 already has this support wende we can just pass it in headers Range bytes=0-1024

I added a search func which queries database based on name 


architecture 

service, controller, routes 

here most the logic iswritteno in the controller 




## challenges 

1) spent too much time tinkering with aws 
and configuration but still managed to do it


2)after deploying I had an authorisation error 
which I fixed by writing custom aws rules 

3) had no unique attribute in response , after adding database added the object key as unique key


scope 

for better scalability adding pagination is a good idea I feel

the architecture is still flawed but i learnt a lot and will enhance it 


adding adaptive streaming using ffmpeg is something I wanna implement 


but overall I was able to build from what I knew but I'm eager to learn! 


