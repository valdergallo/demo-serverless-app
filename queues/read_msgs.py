from queues.actions import receive_messages


if __name__ == "__main__":
    while 1:
        receive_messages(max_number=1, wait_time=1)
