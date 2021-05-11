# Botnet_DDOS
Dependencies places in pyproject.toml file  
----------------
## Setup
~~~bash
# Poetry 
python3 -m pip install poetry           # or
pip3 install poetry
~~~
or
~~~bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
~~~
----------------
## Virtual Environment
~~~bash
# Update or install dependencies
poetry install

# Enter Virtual Environment
poetry shell

# Add Dependency
poetry add <package-name>
~~~

## Run Master
Has to be run as super user
~~~bash
python master.py
~~~

## Run Slave [Bot]
~~~bash
python slave.py
~~~

## Master Commands
~~~bash
ping            -   To check available machines
kill            -   To Stop all slaves
exit            -   To exit master
help            -   To display this help
up              -   Display List of Up Slaves
add-slave       -   To Add Slave
    usage : add-slave -h\--host target_ip
        target_ip   -   Target IP Address to Addd
remove-slave    -   To Remove Slave
    usage : remove-slave -h\--host target_ip
        target_ip   -   Target IP Address to Remove
attack          -   To Start Attack
    usage : attack -h\--host target_ip -p\--port target_port -m\--mode mode -c\--count count -d\--duration duration -s\--slaves slaves -t\--type type
        target_ip   -   Target IP to Attack
        target_port -   Targe Port or Port Range [eg.1000 or 1000-2000]
                        Default : 'all'
        mode        -   Mode of attack  ['botnet'|'virtual']
                        Default : 'botnet'
        count       -   Number of packets to send 
                        Default : 100
        duration    -   Time To Keep Attack Live (in seconds)
                        Default : 30    
        slaves      -   Number of Slaves to Use
                        Default : 'all'
        type        -   Type of Attack 
                        Default = 0
                            0   -   TCP
                            1   -   UDP
                            2   -   HTTP GET
list            -   To List Active Attacks 
stop            -   Stop Attack
    usage : stop -n\--number n
        n           -   Attack Number To Stop
~~~
