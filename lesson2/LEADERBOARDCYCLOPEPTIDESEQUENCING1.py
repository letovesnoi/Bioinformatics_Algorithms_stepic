__author__ = 'lenk'

def getCycloSpectrumPeptide(ip, listP):
    tempCyclospectrum = [0]
    peptide = listP[ip][:]
    for i in range(len(listP[ip]) - 2):
        peptide.append(listP[ip][i])
    for count in range(1, len(listP[ip])):
        for pos in range(len(listP[ip])):
            Pp = peptide[pos:pos + count]
            sum = 0
            for i in range(count):
                sum = sum + Pp[i]
            tempCyclospectrum.append(sum)
    sum = 0
    for i in range(len(listP[ip])):
        sum = sum + peptide[i]
    tempCyclospectrum.append(sum)
    tempCyclospectrum.sort()
    return tempCyclospectrum

def cut(N, listP, massP, Spectrum):
    mScore = []
    indel = []
    for ip in range(len(listP)):
        mScore.append(Score(ip, listP, Spectrum))
    mScore.sort()
    mScore.reverse()
    if N < len(listP):
        ScoreMin = mScore[int(N - 1)]
    elif len(listP) != 0:
        ScoreMin = mScore[-1]
    else:
        return
    countI = 0
    for i in range(len(listP)):
        if Score(i, listP, Spectrum) < ScoreMin:
            indel.append(i)
    for index in indel:
        listP.pop(index - countI)
        massP.pop(index - countI)
        countI += 1
    for i in range(len(indel)):
        indel.pop()

def Score(ip, listP, Spectrum):
    countMatch = 0
    l = 0
    expSpectrum = getCycloSpectrumPeptide(ip, listP)
    for i in range(len(expSpectrum)):
        if Spectrum[l] == expSpectrum[i]:
            countMatch += 1
            l += 1
            if l == len(Spectrum):
                return countMatch
        else:
            while expSpectrum[i] > Spectrum[l]:
                l += 1
                if l == len(Spectrum):
                    return countMatch
            if expSpectrum[i] == Spectrum[l]:
                countMatch += 1
                l += 1
    return countMatch

def expand(mass, listP, massP):
    tempL = len(listP)
    for ip in range(tempL):
        for i in range(len(mass)):
            k = listP[ip][:]
            k.append(mass[i])
            listP.append(k)
            temp = int(massP[ip]) + int(mass[i])
            massP.append(temp)
    for ip in range(tempL):
        listP.pop(0)
        massP.pop(0)

def LEADERBOARDCYCLOPEPTIDESEQUENCING(mass, Spectrum, n):
    massP = []
    arr = []
    listP = []
    begF = 1
    ScorePeptide = 0
    LeaderPeptide = ''
    Spectrum.sort()
    parentMass = int(Spectrum[-1])
    for i in range(len(mass)):
        listP.append([mass[i]])
        massP.append(mass[i])
    while len(listP) != 0 or begF == 1:
        begF = 0
        f1 = open('output.txt', 'w')
        for ip in range(len(listP)):
            if int(massP[ip]) == int(parentMass):
                if Score(ip, listP, Spectrum) > ScorePeptide:
                    iLeaderPeptide = ip
                    LeaderPeptide = listP[iLeaderPeptide]
                    ScorePeptide = Score(iLeaderPeptide, listP, Spectrum)
            elif int(massP[ip]) > int(parentMass):
                arr.append(ip)
        countI = 0
        for index in arr:
            listP.pop(index - countI)
            massP.pop(index - countI)
            countI += 1
        temp = len(arr)
        for i in range(temp):
            arr.pop()
        cut(n, listP, massP, Spectrum)
        print('listP', listP)
        expand(mass, listP, massP)
    for i in range(len(LeaderPeptide) - 1):
        f1.write(str(LeaderPeptide[i]))
        f1.write('-')
    f1.write(str(LeaderPeptide[-1]))
    f1.close()

def main():
    mass = [57, 71, 87, 97,	99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]
    Spectrum = []
    Inp = []
    with open('input.txt', 'r') as f:
        n = int(f.readline())
        Inp.append(f.readline().split())
        for i in range(len(Inp[0])):
            Spectrum.append(int(Inp[0][i]))
    f.close()
    LEADERBOARDCYCLOPEPTIDESEQUENCING(mass, Spectrum, n)

main()