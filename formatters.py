def deletePropsFromStruct(data, delete):
    for item in delete:
        if item in data:
            del data[item]

    return data

def drillForProp(data, parent, child):
    if parent in data:
        childVal = data[parent].pop(child, None)
        data.pop(parent, None)
    
    if childVal:
        data[child] = childVal

    return data


