Grab utilities - gutils
=====================================================================================
### What is it:
It is a set of utilities in Grab, including TM4J client, Slack client, Gitlab client, Gamma client, endpoints helper, etc

### How to use it:
#### TM4J Client
tm4j_client = TM4JClient() with optional parameters: Jira_url, username and password

It leverages TM4J official lib and provides other most used functions to communicate with TM4J

#### Slack Client
slack_client = SlackClient() with mandatory parameter: slack user token

#### Gitlab Client
gitlab_client = GitlabClient() with mandatory parameter: gitlab user token

#### Gamma Client
gamma_client = GammaClient()

#### Endpoints Helper
In endpoints_helper, it provides some useful endpoint handlers

#### Miscellaneous
Decorator retry will help functions stable by retrying
