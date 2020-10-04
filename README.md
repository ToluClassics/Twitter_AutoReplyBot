<h1>Twitter Bot to Auto-Reply Tweets using AWS Lambda and Tweepy</h1>
<p>Twitter Bot created to automatically reply posts with a custom message on twitter</p>

<p>To replicate this app, follow the steps below:</p>
<ul>
  <li><a href:"https://developer.twitter.com/en/apply-for-access">Create a twitter developer account here</a></li>
  <li>Create an AWS account or if you have one sign in to your management console</li>
  <li>Store your credentials as parameter in the aws parameter store</li>
  <li>From your management console, switch to the Lambda panel</li>
  <li>Next, you are going to create a lambda function with the python runtime</li>
  <li>Ensure that your Lambda role allows you access to parameter store</li>
  <li>Create a folder and install a python virtual environment in that folder with the code <code>python -m venv v-env</code></li>
  <li>Activate the virtual environment <code>$ source v-env/scripts/activate</code></li>
  <li>Install the tweepy and boto3 packages <code>pip install tweepy boto3</code></li>
  <li>Download the <a href="https://github.com/ToluClassics/Twitter_ReplyBot/blob/main/Twitter_Bot/lambda_function.py">lambda_function.py</a> and include it in your code folder</li>
  <li>Copy the lamda_function.py to the "lib/site-packages" folder and zip all the files in the folder</li>
  <li>On your lambda config panel, search for upload a zip file and upload your zipped site-packages folder</li>
  <li>Add your custom message and <b>accounts</b> to auto reply as environmental variables</li>
  <li>Create a cloudwatch rule to trigger your lambda function over a given period</li>
  <li>And you are good to go!!!!!</li>
</ul>
