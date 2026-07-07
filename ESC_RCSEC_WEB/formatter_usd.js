/**
 * RC Section Calculator - 강도설계법(USD) Output Formatter
 * 도로교설계기준 강도설계법(2010) 계산과정 출력
 *
 * formatNumber / formatInt 은 formatter.js 에 정의된 것을 재사용한다.
 */

function getMomentTextUSD(calc) {
    let text = '';

    text += '='.repeat(70) + '\n';
    text += '                    휨모멘트 검토 (강도설계법)\n';
    text += '='.repeat(70) + '\n\n';

    text += '1) 단면제원 및 설계가정\n';
    text += `   fck = ${formatInt(calc.fck)} MPa, fy = ${formatInt(calc.fy)} MPa, φf = ${formatNumber(calc.phif, 2)}, φv = ${formatNumber(calc.phiv, 2)}, Es = ${formatInt(calc.Es)} MPa\n\n`;

    text += `   B = ${formatNumber(calc.B, 1)} mm, H = ${formatNumber(calc.H, 1)} mm, d = ${formatNumber(calc.D, 1)} mm, 피복 = ${formatNumber(calc.Dc, 1)} mm\n`;
    text += `   Mu = ${formatNumber(calc.Mun, 0)} N.mm, Vu = ${formatNumber(calc.Vun, 0)} N, Nu = ${formatNumber(calc.Nun, 0)} N\n\n`;

    text += '2) 재료상수\n';
    text += `   εcu    : 콘크리트 극한변형률                         = ${formatNumber(calc.epscu, 4)}\n`;
    text += `   β1     : 등가직사각형 응력블록 깊이계수              = ${formatNumber(calc.beta1, 4)}\n`;
    text += `   Ec     : 콘크리트 탄성계수 (8500·∛(fck+8))          = ${formatNumber(calc.Ec, 1)} MPa\n\n`;

    text += '3) 필요철근량 산정\n';
    text += '   Mu / φf = As x fy x (d - a / 2),   a = As x fy / (0.85 x fck x b)\n';
    text += '   위 식을 As 에 대한 이차방정식으로 정리하여 필요철근량을 구한다.\n';
    text += `   Asreq = ${formatNumber(calc.Asreq, 1)} mm²\n\n`;

    const ratio = calc.Asreq > 0 ? calc.Asuse / calc.Asreq : 0;
    text += `4) 사용철근량 : Asuse = ${formatNumber(calc.Asuse, 1)} mm², 철근도심 : dc = ${formatNumber(calc.Dc, 1)} mm [ 사용율 = ${formatNumber(ratio, 3)} ]\n`;
    text += `      1단 : ${calc.rebarid}${formatInt(calc.AsDia1)} - ${formatInt(calc.AsNum1)} EA (= ${formatNumber(calc.Asuse1 * calc.AsNum1, 1)} mm², dc1 = ${formatNumber(calc.Dc1, 1)} mm)\n`;
    text += `      2단 : ${calc.rebarid}${formatInt(calc.AsDia2)} - ${formatInt(calc.AsNum2)} EA (= ${formatNumber(calc.Asuse2 * calc.AsNum2, 1)} mm², dc2 = ${formatNumber(calc.Dc2, 1)} mm)\n`;
    text += `      3단 : ${calc.rebarid}${formatInt(calc.AsDia3)} - ${formatInt(calc.AsNum3)} EA (= ${formatNumber(calc.Asuse3 * calc.AsNum3, 1)} mm², dc3 = ${formatNumber(calc.Dc3, 1)} mm)\n\n`;

    text += '5) 철근량 검토\n';
    text += `   As,min = (0.25 √fck / fy) x b x d = ${formatNumber(calc.Asmin1, 1)} mm²\n`;
    text += `          = (1.4 / fy) x b x d = ${formatNumber(calc.Asmin2, 1)} mm²\n`;

    if (calc.Asuse >= calc.Asmin) {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² ≥ As,min = ${formatNumber(calc.Asmin, 1)} mm²  ∴ O.K\n`;
    } else {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² < As,min = ${formatNumber(calc.Asmin, 1)} mm²  ∴ N.G\n`;
    }

    text += `   ρb = 0.85 x β1 x (fck/fy) x 600/(600+fy) = ${formatNumber(calc.rhob, 5)}\n`;
    text += `   As,max = 0.75 x ρb x b x d = ${formatNumber(calc.Asmax, 1)} mm²\n`;
    if (calc.Asuse <= calc.Asmax) {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² ≤ As,max = ${formatNumber(calc.Asmax, 1)} mm²  ∴ O.K\n\n`;
    } else {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² > As,max = ${formatNumber(calc.Asmax, 1)} mm²  ∴ N.G (과다철근)\n\n`;
    }

    text += '6) 등가응력블록 및 연성 검토\n';
    text += '   a = As x fy / (0.85 x fck x b)\n';
    text += `     = ${formatNumber(calc.Asuse, 1)} x ${formatInt(calc.fy)} / (0.85 x ${formatInt(calc.fck)} x ${formatNumber(calc.B, 1)}) = ${formatNumber(calc.a, 1)} mm\n`;
    text += `   c = a / β1 = ${formatNumber(calc.a, 1)} / ${formatNumber(calc.beta1, 3)} = ${formatNumber(calc.cc, 1)} mm\n`;
    text += '   εt = (d - c) / c x εcu\n';
    text += `      = (${formatNumber(calc.D, 1)} - ${formatNumber(calc.cc, 1)}) / ${formatNumber(calc.cc, 1)} x ${formatNumber(calc.epscu, 4)} = ${formatNumber(calc.epst, 5)}\n`;
    if (calc.epst >= calc.epsy) {
        text += `   εt ≥ εy = ${formatNumber(calc.epsy, 5)}  ∴ 인장철근 항복 O.K\n\n`;
    } else {
        text += `   εt < εy = ${formatNumber(calc.epsy, 5)}  ∴ 인장철근 미항복 N.G\n\n`;
    }

    text += '7) 설계 휨강도 산정\n';
    text += '   Mn = As x fy x (d - a / 2)\n';
    text += `      = ${formatNumber(calc.Asuse, 1)} x ${formatInt(calc.fy)} x (${formatNumber(calc.D, 1)} - ${formatNumber(calc.a, 1)} / 2) = ${formatNumber(calc.Mn, 1)} N.mm\n`;
    text += `   φMn = ${formatNumber(calc.phif, 2)} x ${formatNumber(calc.Mn, 1)}\n`;

    if (calc.Mr >= calc.Mun) {
        text += `       = ${formatNumber(calc.Mr, 1)} N.mm  ≥ Mu = ${formatNumber(calc.Mun, 1)} N.mm  ∴ O.K  [S.F = ${formatNumber(calc.Msf, 3)}]\n`;
    } else {
        text += `       = ${formatNumber(calc.Mr, 1)} N.mm  < Mu = ${formatNumber(calc.Mun, 1)} N.mm  ∴ N.G  [S.F = ${formatNumber(calc.Msf, 3)}]\n`;
    }

    return text;
}

function getShearTextUSD(calc) {
    let text = '';

    text += '='.repeat(70) + '\n';
    text += '                    전단력 검토 (강도설계법)\n';
    text += '='.repeat(70) + '\n\n';

    text += '8) 콘크리트 전단강도 Vc\n';
    text += '   Vc = (1/6) x (1 + Nu/(14·Ag)) x √fck x b x d\n';
    text += `      = (1/6) x ${formatNumber(calc.axialFactor, 3)} x √${formatInt(calc.fck)} x ${formatNumber(calc.B, 1)} x ${formatNumber(calc.D, 1)}\n`;
    text += `      = ${formatNumber(calc.Vc, 0)} N\n`;
    text += `   φVc   = ${formatNumber(calc.phiv, 2)} x ${formatNumber(calc.Vc, 0)} = ${formatNumber(calc.phiVc, 0)} N\n`;
    text += `   φVc/2 = ${formatNumber(calc.phiVc / 2, 0)} N\n\n`;

    text += `   Av,use = ${formatNumber(calc.Avs, 1)} mm² ( ${calc.rebarid}${formatInt(calc.AvDia)} - ${formatNumber(calc.AvLeg, 0)}ea, C.T.C = ${formatNumber(calc.AvSpace, 1)} mm )\n\n`;

    if (calc.shearCase === 'none') {
        text += '9) 전단설계\n';
        text += `   Vu = ${formatNumber(calc.Vun, 0)} N ≤ φVc/2 = ${formatNumber(calc.phiVc / 2, 0)} N  ∴ 전단철근 불필요\n\n`;
    } else if (calc.shearCase === 'min') {
        text += '9) 전단설계 (최소전단철근)\n';
        text += `   φVc/2 = ${formatNumber(calc.phiVc / 2, 0)} N < Vu = ${formatNumber(calc.Vun, 0)} N ≤ φVc = ${formatNumber(calc.phiVc, 0)} N  ∴ 최소전단철근 배치\n`;
        text += `   ρv,min = max(0.0625√fck/fy, 0.35/fy) = ${formatNumber(calc.rhovmin, 6)}\n`;
        if (calc.rhovuse >= calc.rhovmin) {
            text += `   ρv,use = Av / (s x b) = ${formatNumber(calc.rhovuse, 6)} ≥ ρv,min  ∴ O.K\n`;
        } else {
            text += `   ρv,use = Av / (s x b) = ${formatNumber(calc.rhovuse, 6)} < ρv,min  ∴ N.G\n`;
        }
        text += `   s = ${formatNumber(calc.AvSpace, 1)} mm ≤ s,max = ${formatNumber(calc.smax, 1)} mm  ${calc.AvSpace <= calc.smax ? '∴ O.K' : '∴ N.G'}\n\n`;
    } else {
        text += '9) 전단설계 (전단보강)\n';
        text += `   Vu = ${formatNumber(calc.Vun, 0)} N > φVc = ${formatNumber(calc.phiVc, 0)} N  ∴ 전단보강 필요\n\n`;
        text += '   Vs = Av x fy x d / s\n';
        text += `      = ${formatNumber(calc.Avs, 1)} x ${formatInt(calc.fy)} x ${formatNumber(calc.D, 1)} / ${formatNumber(calc.AvSpace, 1)} = ${formatNumber(calc.Vs, 0)} N\n`;
        text += `   Vs,max = (2/3)√fck x b x d = ${formatNumber(calc.Vsmax, 0)} N  ${calc.Vs <= calc.Vsmax ? '(Vs ≤ Vs,max O.K)' : '(Vs > Vs,max N.G, 단면증대필요)'}\n\n`;
        text += '   φVn = φ x (Vc + Vs)\n';
        text += `       = ${formatNumber(calc.phiv, 2)} x (${formatNumber(calc.Vc, 0)} + ${formatNumber(calc.Vs, 0)}) = ${formatNumber(calc.Vr, 0)} N\n`;
        if (calc.Vr >= calc.Vun) {
            text += `   φVn = ${formatNumber(calc.Vr, 0)} N ≥ Vu = ${formatNumber(calc.Vun, 0)} N  ∴ O.K\n`;
        } else {
            text += `   φVn = ${formatNumber(calc.Vr, 0)} N < Vu = ${formatNumber(calc.Vun, 0)} N  ∴ N.G\n`;
        }
        text += `   s = ${formatNumber(calc.AvSpace, 1)} mm ≤ s,max = ${formatNumber(calc.smax, 1)} mm  ${calc.AvSpace <= calc.smax ? '∴ O.K' : '∴ N.G'}\n\n`;
    }

    return text;
}

function getServiceTextUSD(calc) {
    let text = '';

    text += '='.repeat(70) + '\n';
    text += '                    사용성 검토 (균열, 강도설계법)\n';
    text += '='.repeat(70) + '\n\n';

    text += '10) 균열 검토 (탄성 균열단면)\n';
    text += `    n = Es / Ec = ${formatInt(calc.Es)} / ${formatNumber(calc.Ec, 1)} = ${formatInt(calc.nr)}\n`;
    text += `    fr = 0.63√fck = ${formatNumber(calc.fr, 3)} MPa,  Mcr = fr·Ig/yt = ${formatNumber(calc.Mcr, 0)} N.mm\n`;
    text += `    균열단면 중립축 x = ${formatNumber(calc.xcr, 2)} mm,  Icr = ${formatNumber(calc.Icr, 0)} mm⁴\n\n`;

    text += '    철근 응력 (사용하중)\n';
    text += `    fs,1 = n·Ms1·(d-x)/Icr = ${formatNumber(calc.fs1, 2)} MPa\n`;
    text += `    fs,5 = n·Ms5·(d-x)/Icr = ${formatNumber(calc.fs5, 2)} MPa\n\n`;

    text += '    콘크리트 압축응력 (사용하중)\n';
    text += `    fc,1 = Ms1·x/Icr = ${formatNumber(calc.fc1, 2)} MPa\n`;
    text += `    fc,5 = Ms5·x/Icr = ${formatNumber(calc.fc5, 2)} MPa\n\n`;

    text += '    허용응력\n';
    text += `    fca = 0.6·fck = ${formatNumber(calc.fca, 2)} MPa (콘크리트)\n`;
    if (calc.fc1 <= calc.fca) {
        text += `    fc,1 = ${formatNumber(calc.fc1, 2)} MPa ≤ fca = ${formatNumber(calc.fca, 2)} MPa  ∴ O.K\n\n`;
    } else {
        text += `    fc,1 = ${formatNumber(calc.fc1, 2)} MPa > fca = ${formatNumber(calc.fca, 2)} MPa  ∴ N.G\n\n`;
    }

    text += '11) 간접균열검토\n';
    text += `    철근직경에 의한 허용응력 fsad = ${formatNumber(calc.fsad, 0)} MPa\n`;
    text += `    철근간격에 의한 허용응력 fsas = ${formatNumber(calc.fsas, 0)} MPa\n`;
    text += `    fsa = max(fsad, fsas) = ${formatNumber(calc.fsaf, 0)} MPa\n`;
    if (calc.fs1 <= calc.fsaf) {
        text += `    fs,1 = ${formatNumber(calc.fs1, 2)} MPa ≤ fsa = ${formatNumber(calc.fsaf, 0)} MPa  ∴ O.K\n`;
    } else {
        text += `    fs,1 = ${formatNumber(calc.fs1, 2)} MPa > fsa = ${formatNumber(calc.fsaf, 0)} MPa  ∴ N.G\n`;
    }

    return text;
}

function getFullCalcTextUSD(calc) {
    let text = '';

    text += '╔' + '═'.repeat(68) + '╗\n';
    text += '║' + '              RC 단면 검토 계산서 (강도설계법)                      ' + '║\n';
    text += '╚' + '═'.repeat(68) + '╝\n\n';

    text += getMomentTextUSD(calc);
    text += '\n';
    text += getShearTextUSD(calc);
    text += '\n';
    text += getServiceTextUSD(calc);

    return text;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getMomentTextUSD, getShearTextUSD, getServiceTextUSD, getFullCalcTextUSD };
}
