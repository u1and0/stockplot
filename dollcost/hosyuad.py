def dob(se):
    position = np.zeros(len(se))  # seと同じ長さの配列を作成
    for i in se.index[:-1]:
        if se[i+1] - se[i] > 0:
            position[i]=se[i]
    return position

[se[i] if se[i+1]>se[i] else 0 for i in se.index[:-1]]

np.where(se[i], 0, se[i+1]>se[i])