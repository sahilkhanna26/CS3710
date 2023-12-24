import hashlib
import binascii
import rsa
import sys
import random
from datetime import datetime





# gets the hash of a file; from https://stackoverflow.com/a/44873382
def hashFile(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

# given an array of bytes, return a hex reprenstation of it
def bytesToString(data):
    return binascii.hexlify(data)


# given a hex reprensetation, convert it to an array of bytes
def stringToBytes(hexstr):
    return binascii.a2b_hex(hexstr)

# Load the wallet keys from a filename
def loadWallet(filename):
    with open(filename, mode='rb') as file:
        keydata = file.read()
    privkey = rsa.PrivateKey.load_pkcs1(keydata)
    pubkey = rsa.PublicKey.load_pkcs1(keydata)
    return pubkey, privkey

# save the wallet to a file
def saveWallet(pubkey, privkey, filename):
    # Save the keys to a key format (outputs bytes)
    pubkeyBytes = pubkey.save_pkcs1(format='PEM')
    privkeyBytes = privkey.save_pkcs1(format='PEM')
    # Convert those bytes to strings to write to a file (gibberish, but a string...)
    pubkeyString = pubkeyBytes.decode('ascii')
    privkeyString = privkeyBytes.decode('ascii')
    # Write both keys to the wallet file
    with open(filename, 'w') as file:
        file.write(pubkeyString)
        file.write(privkeyString)
    return

def cryptoName():
    return "KhannaCoin (TM)"




def create_inital_block():
    filename = "block_0.txt"
    text = "\"KhannaCoin: like Ghana but with a K and 2 N's\""

    with open("block_tracker.txt", "w") as f:
        print(filename, file=f)

    with open(filename, "w") as f:
        print(text, "\n", file=f)




def createKey(filename):
    (pubkey, privkey) = rsa.newkeys(1024)
    saveWallet(pubkey,privkey,filename)

def getTag(filename):
    hashed = hashFile(filename)
    tag = hashed[0:16]
    return tag

def createTransactionStatement_fund(to, amount, date, filename):
    date = str(date)
    text =  "From: Big_dog_khanna"+"\n" +"To: "+ to +"\n" +"Amount: " + amount +"\n"+ "Date: " + date

    with open(filename, "w") as f:
        print(text,file=f)
        print("\n",file=f)

def createTransactionStatement_transfer(frm, to, amount, date, filename, source_file):
    date = str(date)
    text =  "From:"+ frm +"\n" +"To:"+ to +"\n" +"Amount:" + amount +"\n"+ "Date: " + date

    with open(filename, "w") as f:
        print(text,file=f)

    (pubkey, privkey) = loadWallet(source_file)

    encoded = text.encode()
    signature = rsa.sign(encoded, privkey, 'SHA-256')
    decoded =  binascii.hexlify(signature)
    decoded = decoded.decode()
    # hashed = hashFile(filename)
    # encoded = hashed.encode('ascii')
    # signature = rsa.encrypt(encoded,privkey)
    # decoded = binascii.hexlify(signature)
    # decoded = decoded.decode()
    decoded = decoded.strip()

    with open(filename, "w") as f:
        print(text, "\n", decoded, file=f)

    #verifying
    # decoded = decoded.encode()
    # dec = binascii.unhexlify(decoded)
    # ret_val = rsa.verify(encoded,dec,pubkey)
    # print(ret_val)

    #decrypting

    # s = rsa.encrypt(signature,pubkey)
    # print(s)


    # hashed = hashFile(filename)
    # encoded = hashed.encode('ascii')
    # encrypted = rsa.encrypt(encoded,privkey)
    # decrypted = rsa.decrypt(encrypted,pubkey)
    # decoded = decrypted.decode('ascii')
    #
    #
    # x = bytesToString(encrypted)
    # print(x)
    #
    # print("Hashed:", hashed)
    # print("decoded")



def calculate_balance(taga):
    balance = 0

    file1 = open('block_tracker.txt', 'r')
    lines = file1.readlines()
    block_list = []

    for line in lines:
        bloc = line.strip("\n")
        block_list.append(bloc)

    for block in block_list:
        file1 = open(block, 'r')
        lines = file1.readlines()

        for line in lines:
            if taga in line:
                str1 = "transferred "
                str2 = " to"
                i1 = line.index(str1)
                i2 = line.index(str2)

                amount = line[i1 + len(str1):i2]
                amount = int(amount)
                if (line.index(taga) == 0):
                    balance = balance - amount
                    # print(balance)

                else:
                    balance = balance + amount
                    # print(balance)

            else:
                pass
    file2 = open('mempool.txt', 'r')
    lines2 = file2.readlines()
    transactions = []

    for line2 in lines2:
        transaxn = line2.strip("\n")
        transactions.append(transaxn)

    for t in transactions:
        if taga in t:

            str1 = "transferred "
            str2 = " to"
            i1 = t.index(str1)
            i2 = t.index(str2)

            amount = t[i1 + len(str1):i2]
            amount = int(amount)
            if (t.index(taga) == 0):
                balance = balance - amount
                    # print(balance)

            else:
                balance = balance + amount
                    # print(balance)
    return (balance)

def check_balance(taga, transaction_name):
    balance = calculate_balance(taga)
    print(balance)
    file1 = open(transaction_name, 'r')
    lines = file1.readlines()
    amount = 0
    for line in lines:
        if ("Amount" in line):
            l = len(line)
            substr = "Amount:"
            l2 = len(substr)
            # print(line)
            amount = line[l2:l]
            amount = int(amount)


        else:
            pass
    if(amount<balance):
        return True
    else:
        return False

def check_signature(transaction_name, pubkey):
    file1 = open(transaction_name, 'r')
    lines = file1.readlines()
    text = ""
    n = len(lines)
    for i in range(0,n-1):
        line = lines[i]
        text = text + line

    text = text.strip("\n")
    text = text.strip()
    # print(text)


    message = text.encode()
    # print(message)

    # verifying
    # decoded = decoded.encode()
    # dec = binascii.unhexlify(decoded)
    # ret_val = rsa.verify(encoded,dec,pubkey)
    # print(ret_val)

    signature = lines[n-1]
    signature = signature.strip()
    enc = signature.encode()
    value = binascii.unhexlify(enc)
    hasher = rsa.verify(message,value,pubkey)
    if(hasher == "SHA-256"):
        return True
    else:
        return False

def create_new_block(difficulty):
    file1 = open('block_tracker.txt', 'r')
    lines = file1.readlines()
    # print(lines)

    num_blocks = len(lines)
    prev_block = lines[num_blocks-1]
    prev_block = prev_block.strip("\n")



    hashed = hashFile(prev_block)

    file1 = open("mempool.txt", "r")
    lines2 = file1.readlines()
    lines3 = []
    for line in lines2:
        line = line.strip()
        lines3.append(line)


    #clear mempool
    with open("mempool.txt", "w") as f:
        pass





    filename = "block_"+str(num_blocks) + ".txt"
    # print(filename)

    with open(filename, "w") as f:
        print(hashed, file=f)
        for l in lines3:
            print(l,file=f)

        # nonce value
    for i in range(0, 100000000000):
        if(i==0):
            with open(filename, "a") as f:
                f.write(str(i))
        else:
            with open(filename, 'r') as file:
                data = file.readlines()
            n = len(data)
            data[n-1] = str(i)
            with open(filename, 'w') as file:
                file.writelines(data)

        hashed_val = hashFile(filename)
        leading = hashed_val[0:int(difficulty)]
        compare_val = "0"*int(difficulty)
        compare_val = str(compare_val)
        # print("leading:",leading)
        # print(compare_val)
        if(leading == compare_val):
            print("Mempool transactions moved to", filename, "and mined with difficulty", difficulty, "and nonce",i)
            i = 100000000000

            break
        else:
            i = i+1



    file1 = open("block_tracker.txt", "a")
    file1.write(filename + "\n")
    file1.close()

def validate_chain():
    file1 = open('block_tracker.txt', 'r')
    lines = file1.readlines()


    block_list = []
    for line in lines:
        block = line.strip("\n")
        block_list.append(block)

    if(len(block_list) == 1):
        if(block_list[0] == "block_0.txt"):
            return True
        else:
            return False
    else:
        for i in range(1,len(block_list)-1):
            file_1 = block_list[i]
            file_2 = block_list [i+1]
            hashed = hashFile(file_1)
            f = open(file_2, "r")
            lines2 = f.readlines()

            hashed2 = lines2[0].strip("\n")
            if(hashed != hashed2):
                return False
        return True





# def create_mempool():
#
# def save_to_mempool():

def main():
    global sender
    sender = "Big_dog_khanna"
    (pubkey, privkey) = rsa.newkeys(1024)
    s_pubkey = pubkey
    s_privkey = privkey
    sender_filename = "big_dog_wallet.txt"
    saveWallet(s_pubkey, s_privkey, sender_filename)
    fund_tag = getTag(sender_filename)

    i=1
    while i < len(sys.argv):
        if(sys.argv[i] == "name"):
            name = cryptoName()
            print(name)
        elif(sys.argv[i] == "genesis"):
            create_inital_block()
            print("Genesis block created in 'block_0.txt'")

        elif (sys.argv[i] == "generate"):
            i = i+1
            filename = sys.argv[i]
            createKey(filename)
            tag = getTag(filename)
            print("New wallet generated in",filename,"with tag",tag)

        elif (sys.argv[i]== "address"):
            i=i+1
            filename = sys.argv[i]
            tag = getTag(filename)
            print(tag)

        elif (sys.argv[i] == "fund"):
            i = i+1
            taga = sys.argv[i]
            i= i+1
            amount = sys.argv[i]
            i=i+1
            filename = sys.argv[i]
            #funding will go from sender to this tag
            createTransactionStatement_fund(taga,amount,datetime.now(),filename)
            print("Funded wallet", taga, "with", amount,"KhannaCoin on",datetime.now())

        elif(sys.argv[i] == "transfer"):
            i = i+1
            source_file = sys.argv[i]
            i = i+1
            to_tag = sys.argv[i]
            i = i+1
            amount = sys.argv[i]
            i = i+1
            filename = sys.argv[i]

            source_tag = getTag(source_file)
            date = datetime.now()
            createTransactionStatement_transfer(source_tag,to_tag,amount,date,filename,source_file)
            print("Transferred",amount, "from", source_file, "to", to_tag, "and the statement to", filename, "on", date)

        elif(sys.argv[i] == "balance"):
            i = i+1
            taga = sys.argv[i]
            print( calculate_balance(taga))


        elif (sys.argv[i] == "verify"):
            i = i+1
            wallet_name = sys.argv[i]
            i=i+1
            transaction_name = sys.argv[i]
            tag = getTag(wallet_name)

            (pubkey,privkey)= loadWallet(wallet_name)

            file1 = open(transaction_name, 'r')
            lines = file1.readlines()
            from_val = lines[0]
            to_val = lines[1]
            amount_val = lines[2]
            date_val = lines[3]
            substr1 = "from: "
            substr2 = "to: "
            substr3 = "amount: "
            substr4 = "date: "
            s1 = len(substr1)
            s2 = len(substr2)
            s3 = len(substr3)
            s4 = len(substr4)
            from_val = from_val[s1 - 1:len(from_val)]
            to_val = to_val[s2 - 1:len(to_val)]
            amount_val = amount_val[s3 - 1:len(amount_val)]
            date_val = date_val[s4:len(date_val)]
            from_val = from_val.strip("\n")
            to_val = to_val.strip("\n")
            amount_val = amount_val.strip("\n")
            date_val = date_val.strip("\n")
            from_val = from_val.strip()
            date_val = date_val.strip()
            amount_val = amount_val.strip()
            to_val = to_val.strip()


            if (from_val == sender):
                #it is a funding request
                text = from_val + " transferred " + amount_val + " to " + to_val + " on " + date_val
                file1 = open("mempool.txt", "a")  # append mode
                file1.write(text + "\n")
                file1.close()
                print("The transaction in file", transaction_name, "with wallet", wallet_name, "is valid, and was written to the mempool")




            else:
                check_1 = check_balance(tag,transaction_name)
                print(check_1)
                check_2 = check_signature(transaction_name,pubkey)
                if (check_1 and check_2 == True):

                    text = from_val + " transferred " + amount_val + " to "+ to_val + " on " + date_val

                    #add to mempool
                    file1 = open("mempool.txt", "a")  # append mode
                    file1.write(text + "\n")
                    file1.close()

                    print("The transaction in file", transaction_name, "with wallet", wallet_name,"is valid, and was written to the mempool")
                else:
                    print (False)


        elif (sys.argv[i] == "mine"):
            i = i+1
            difficulty = sys.argv[i]
            create_new_block(difficulty)

        elif(sys.argv[i] == "validate"):
            x = validate_chain()
            print(x)




        else:
            pass

        i += 1

if __name__ == '__main__':
    main()