import time


def my_sync_function():
    # some sync code here
    time.sleep(1)  # wait for 1 second

def main():
    # call the sync function and wait for it to complete
    my_sync_function()

    # continue with the next line of code
    print("Done")

main()
print("blaa")
main()
print("olee")