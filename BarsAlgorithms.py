def meanN(signal, n=1):
    if n < 1:
        raise ValueError("N must by bigger than 1")
    if len(signal) == 0:
        raise ValueError("Empty signal given")
    y = signal
    out = []
    div = len(y)/n 
    counter = 0.0
    bucket = 0
    for i in y:
        if counter < div:
            bucket += i
            counter += 1
        else: 
            bucket /= counter
            out.append(int(bucket))
            bucket = i
            counter = 1
    if len(out) == 0:
        bucket /= counter
        out.append(int(bucket))
    elif counter > 1:
        lastValue = out[len(out)-1]  
        out[len(out)-1]  = int((lastValue + bucket/counter)/2)
    return out

def maxN(signal, n=1):
    if n < 1:
        raise ValueError("N must by bigger than 1")
    if len(signal) == 0:
        raise ValueError("Empty signal given")
    y = signal
    out = []
    div = len(y)/n 
    counter = 0.0
    buckets = []
    bucket = []
    for i in y:
        if counter < div:
            bucket.append(i)
            counter += 1
        else: 
            buckets.append(bucket)
            bucket = []
            bucket.append(i)
            counter = 1
    if counter > 1:
        buckets[len(buckets)-1] += bucket
    
    for i in buckets:
        out.append(max(i))

    return out
