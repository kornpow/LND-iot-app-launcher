# setting up ZAP wallet to access your odroid node
Using the ZAP wallet is a lot easier than ```lncli```

## Download the ZAP wallet app
1. Go to the [LN-Zap project on github](https://github.com/LN-Zap/zap-desktop/releases).
1. Choose the appropriate release platform for your desktop system, I used ```Zap-linux-x86_64-v0.4.1-beta.AppImage```
1. Download the release to your PC.  On Linux you may need to mark it as executable using ```chmod ugoa+x```
1. Start Zap wallet, e.g. on Linux ```sudo ./Zap-linux-x86_64-v0.4.1-beta.AppImage```
   ![Zap Wallet](https://i.imgur.com/lXmWLAA.png)
1. Choose "Connect to your node", Next and it should prompt you to enter the connection string:
   ![Zap connection](https://i.imgur.com/0VkoMpg.png)
1. LND has a complicated security mechanism for obvious reasons.  It uses [TLS security](https://en.wikipedia.org/wiki/Transport_Layer_Security) (same as in secure web pages) and [macaroons](https://github.com/lightningnetwork/lnd/blob/master/docs/macaroons.md) (similar to cookies).  ZAP needs to have both pieces of information from your LND node in order to connect.  In the next section we will use a utility to collect the information ZAP needs in order to access your Lightning wallet.

## Use lndconnect utility to generate the connection string for ZAP wallet

1. open a command terminal to your node, e.g. using ```~/balena-cli/balena ssh uuid main```
1. on your node, enter the following commands to get the lndconnect utility

    ```export PATH=$PATH:/root/go/bin```

    ```export GOPATH=/root/gocode```

    ```export PATH=$PATH:$GOPATH/bin```

    ```go get github.com/LN-Zap/lndconnect```

    ```cd $GOPATH/src/github.com/LN-Zap/lndconnect/```

    ```go build```

    ```lndconnect --adminmacaroonpath=~/.lnd/data/chain/litecoin/testnet/admin.macaroon -j```


1. this will give you a long string beginning with "```lndconnect:```"
1. paste the lndconnect string into the ZAP wallet connection string screen.
1. lndconnect may have used your external IP address, but may need to change this to your internal network address to be able to access it, e.g. ```192.168.0.107```
1. click next, verify the correct IP address, click next again, and your wallet details should be open.  If it times out with the message "Unable to connect to host", you possibly entered the wrong IP address for your node.
1. ![Zap connected](https://i.imgur.com/A73cKPr.png)



