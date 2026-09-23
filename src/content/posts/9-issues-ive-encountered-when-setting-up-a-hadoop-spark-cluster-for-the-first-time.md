---
title: "9 issues I’ve encountered when setting up a Hadoop/Spark cluster for the first time"
seoTitle: "9 Hadoop/Spark Cluster Setup Errors and How to Fix Them"
seoDescription: "A hands-on guide to 9 common Hadoop and Spark cluster setup errors, from JAVA_HOME not set to spark.yarn.jars. Each issue includes the exact fix that..."
datePublished: 2020-04-26T11:33:50.412Z
dateUpdated: 2026-03-02T10:51:11.861Z
cover: "/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/cover.jpg"
series: "my-data-journey"
hashnodeCuid: "clfmm6zlf000709me6fsx1pr5"
---

In a [previous article](/how-i-set-up-my-first-hadoop-spark-cluster-preparation), we discussed how to prepare the setup of a Hadoop/Spark cluster. Now, preparing the cluster was only the beginning. While there are plenty of resources about setting up Hadoop on a cluster, as a beginner I’ve found it confusing at times and I spent a good dozen hours putting it all together. Therefore, in this article, I’ll document the issues encountered during setting up the Hadoop/Spark cluster and how to solve them. If you wish to give it a try yourself, please review [the tutorial I’ve followed](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2) to set this all up, which I wholeheartedly recommend.

Now, to give you some context, my setup is made by a laptop (which will serve both as a name node and a data node) and Raspberry Pis as another two data nodes, as follows:

![](/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/1.png)

Note that I will be running Spark 2.4.5 and Hadoop 3.2.1.

So, we’ve downloaded, unpacked and moved `hadoop` to `/opt/hadoop`.

Let’s try to start it

```bash
hadoop version
```

Oops!

### JAVA\_HOME\_NOT\_SET

First of all, please do check you have Java installed. If you’d like Spark down the road, keep in mind that the current stable Spark version is [not compatible with Java 11](https://stackoverflow.com/questions/55269788/spark-2-4-java-11-compatibility?noredirect=1&lq=1).

```bash
sudo apt install openjdk-8-jre-headless -y
```

Then, let’s look at the environmental variables. The tutorial (built for Raspbian) recommended setting this environment variable to something like

```markdown
export JAVA_HOME=$(readlink –f /usr/bin/java | sed "s:bin/java::")
```

whereas the following, [inspired from here](https://stackoverflow.com/questions/14325594/working-with-hadoop-localhost-error-java-home-is-not-set/14462600#14462600), made it work for me (on Ubuntu):

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
```

Please also note the environment variables I’ve added to *.bashrc* :

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-arm64
export HADOOP_HOME=/opt/hadoop
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
```

Also, we need to add JAVA\_HOME as above to

`/opt/hadoop/etc/hadoop/hadoop-env.sh`

Let’s try again now:

```bash
hadoop version
```

![](/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/2.png)

Works! Moving forward.

# Permission denied (publickey,password).

So, everything is ready to spin off the Hadoop cluster. The only thing is when running

```bash
start-dfs.sh && start-yarn.sh
```

I keep receiving the following error:

```markdown
localhost: Permission denied (publickey,password).
```

Turns out, multiple things are happening here. First, my user had a different name than the one on the slave nodes, so my SSH authentication was failing. To sort that out, on the master, [I had to set up a config file](https://stackoverflow.com/questions/51822209/hadoop-cluster-hadoop-user-ssh-communication/51830400#51830400) at ***~/.ssh/config*** as follows:

```bash
Host rpi-3
HostName rpi-3
User ubuntu
IdentityFile ~/.ssh/id_rsa

Host rpi-4
HostName rpi-4
User ubuntu
IdentityFile ~/.ssh/id_rsa
```

This made clear what is user I want to use when connecting with SSH.

But this wasn’t all. More importantly, though, it turns out I needed to [SSH into localhost first](https://stackoverflow.com/questions/15195048/hadoop-require-roots-password-after-enter-start-all-sh/39328364#39328364) to be able to run **start-dfs.sh** and **start-yarn.sh** . Moving forward.

### Hadoop cluster setup — java.net.ConnectException: Connection refused

The next error on our list took me a good evening to debug. So when trying to start the cluster with `start-dfs.sh` I was receiving a connection refused error. First, without thinking too much about it, I followed the advice from [here](https://stackoverflow.com/questions/28661285/hadoop-cluster-setup-java-net-connectexception-connection-refused/33553214#33553214) and set up the default server to 0.0.0.0.

The correct answer was in fact to set it to my name node server’s address (in **core-site.xml**) AND to make sure there isn’t an entry in **/etc/hosts** tying that to 127.0.0.1 or localhost. Hadoop doesn’t like that, and I’ve [been warned](https://dev.to/awwsmm/building-a-raspberry-pi-hadoop-spark-cluster-8b2).

![](/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/3.png)

### Nodes not showing up

In a multi-node setup having some nodes missing can steam from a wide array of causes. Wrong configuration, differences in environments and even firewalls can cause issues. Here are a couple of tips on how to make head or tail of it.

#### Check the UIs first

There are several web interfaces exposed in a typical Hadoop stack. Two of them are the **Yarn UI** exposed on port 8088 and **Name Node Information UI** exposed on port 9870. In my case, I had a different number of nodes in HDFS than YARN, which pointed me to investigate and find the issue with my YARN settings.

#### Use jps to see that service is running

Jps is a Java tool, but you can use it to see which Hadoop services are up on a particular machine.

![](/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/4.png)

Is the DataNode up on the given node? Let’s move forward.

#### Dive into Hadoop logs

Hadoop logs are located in the logs subfolder, so in my case /opt/hadoop/logs. Don’t see a particular data node? Ssh into that machine and analyze the logs say for that particular service.

#### Check the configuration files

That’s were most issues could stem from. Review the logs, document yourself what the correct configuration is and apply them. The configuration files are located in */opt/hadoop/etc/hadoop*. Start with the file corresponding to the service you’re trying to debug.

OK, so we’re more or less fine with Hadoop now. What about Spark? I downloaded Spark (without Hadoop) and unpacked it. Now what? Smooth sailing? Not so fast.

### Spark fails to start

If you’ve downloaded Spark standalone, chances are you’d bump into the same issue as I did, so be sure to add the following to `conf/spark-env.sh`

```markdown
export SPARK_DIST_CLASSPATH=$(/path/to/hadoop/bin/hadoop classpath)
```

Credits for this solution go [here](https://stackoverflow.com/questions/42307471/spark-without-hadoop-failed-to-launch/42689980#42689980).

### Pyspark error — Unsupported class file major version 55

Seriously, I’ve warned you above that the current stable Spark version is only compatible with Java 8. [More details on that](https://stackoverflow.com/questions/53583199/pyspark-error-unsupported-class-file-major-version-55/53583241#53583241).

### java.lang.NumberFormatException: For input string: “0x100”

Next, this harmless but annoying message that you’d see once starting the *spark-shell* can be easily fixed by adding an environment variable to **.bashrc**.

```markdown
export TERM=xterm-color
```

Read more about it [here](https://stackoverflow.com/questions/56457685/how-to-fix-the-sbt-crash-java-lang-numberformatexception-for-input-string-0x/56457806#56457806).

### **Spark UI has broken CSS**

When starting a spark-shell or submitting a Spark job, a spark context Web UI is made available at port 4040 on the namenode. In my case, the issue was that the UI had a broken interface, which made using it impossible.

![](/images/9-issues-ive-encountered-when-setting-up-a-hadoop-spark-cluster-for-the-first-time/5.png)

Once again, StackOverflow was my friend. To sort this one, one would need to start a spark-shell and run the following command:

```bash
sys.props.update("spark.ui.proxyBase", "")
```

Credits to the solution [here](https://stackoverflow.com/questions/47875064/spark-ui-appears-with-wrong-format-broken-css/55466574#55466574).

### Property Spark.yarn.jars

When running Spark in a clustered mode on top of a YARN cluster, the Spark .jar classes need to be shipped across to other nodes that don’t have Spark installed. Probably it took me more tinkering to sort it out than it should, but in my case, the solution was to upload it to a location inside HDFS and let the nodes get it from there when they need it.

Creating the archive:

```bash
jar cv0f spark-libs.jar -C $SPARK_HOME/jars/ .
```

Upload to HDFS

```bash
hdfs dfs -put spark-libs.jar /some/path/
```

Then, in *spark-defaults.conf* set

```bash
spark.yarn.archive hdfs://your-name-node:9000/spark-libs.jar
```

Credits to the solution and explanation [here](https://stackoverflow.com/questions/41112801/property-spark-yarn-jars-how-to-deal-with-it).

### Conclusion

This concludes our recap on some errors encountered during setting up Hadoop and Spark as a beginner. We’ll give our cluster a spin, test it out and report it in a future article. Thanks for reading and stay tuned!

*Found it useful? Subscribe to my Analytics newsletter at* [*notjustsql.com*](https://www.notjustsql.com)*.*
