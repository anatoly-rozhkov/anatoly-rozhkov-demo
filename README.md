### Line Provider

Hello, I'm assuming you'll be testing this on Monday morning. So, here are some coffee and snacks from me 
to lighten your mood  ☕🥐 (those are free btw)

### Description
Line provider is a basic FastAPI that can perform CRUD operations on a event object.
Event objects are stored in memory in a singleton class called DataStorage.
Creation and updates on events publishes them to a RabbitMQ queue for Bet Maker.

### Requirements
Create .env and copy the contents of .env.example to it.
(Sorry for the bother guys, I'm not the one making rules)

In the root directory, run:
```
make start
```
You can access swagger here, I've set the examples so that it would be easier to test.
http://127.0.0.1:8080/docs

### Considerations
Deadline: I've made the deadline being a time field that accepts the num of seconds from now as the effective deadline.

### Tests
```
make test
```
I've left the tests as is for this app because Bet Maker already has extended tests to show off my skills.
### Shutdown
```
make stop
```

### Bet Maker
https://github.com/anatoly-rozhkov/anatoly-rozhkov-demo-2