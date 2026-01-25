/**
 * RC Section Calculator - Output Formatter
 * Converted from Python (sec_front_ver031.py)
 */

function formatNumber(num, decimals = 1) {
    if (num === undefined || num === null || isNaN(num)) return '0';
    return num.toFixed(decimals);
}

function formatInt(num) {
    if (num === undefined || num === null || isNaN(num)) return '0';
    return Math.round(num).toString();
}

function getMomentText(calc) {
    let text = '';

    text += '=' .repeat(70) + '\n';
    text += '                    휨모멘트 검토\n';
    text += '=' .repeat(70) + '\n\n';

    text += '1) 단면제원 및 설계가정\n';
    text += `   fck = ${formatInt(calc.fck)} MPa, fy = ${formatInt(calc.fy)} MPa, Øc = ${formatNumber(calc.Oc, 2)}, Øs = ${formatNumber(calc.Os, 2)}, Es = ${formatInt(calc.Es)} MPa\n\n`;

    text += `   B = ${formatNumber(calc.B, 1)} mm, H = ${formatNumber(calc.H, 1)} mm, d = ${formatNumber(calc.D, 1)} mm, 피복 = ${formatNumber(calc.Dc, 1)} mm\n`;
    text += `   Mu = ${formatNumber(calc.Mun, 0)} N.mm, Vu = ${formatNumber(calc.Vun, 0)} N\n\n`;

    text += '2) 콘크리트 재료상수\n';
    text += `   n      : 상승 곡선부의 형상을 나타내는 지수          = ${formatNumber(calc.neps, 4)}\n`;
    text += `   εco,r  : 최대응력에 처음 도달했을때의 변형률          = ${formatNumber(calc.epsco, 5)}\n`;
    text += `   εcu,r  : 극한변형률                                  = ${formatNumber(calc.epscu, 5)}\n`;
    text += `   αcc    : 유효계수                                    = ${formatNumber(calc.alphacc, 2)}\n`;
    text += `   fcd    : 콘크리트 설계압축강도                       = ${formatNumber(calc.fcd, 2)} MPa\n`;
    text += `   fcm    : 평균압축강도(fck+Δf)                        = ${formatNumber(calc.fcm, 2)} MPa\n`;
    text += `   Ec     : 콘크리트 탄성계수                           = ${formatNumber(calc.Ec, 2)} MPa\n`;
    text += `   α      : 압축합력의 평균 응력계수                    = ${formatNumber(calc.alpha, 4)}\n`;
    text += `   β      : 압축합력의 작용점 위치계수                  = ${formatNumber(calc.beta, 4)}\n`;
    text += `   η      : 등가 사각형 응력 블록의 크기계수            = ${formatNumber(calc.eta, 4)}\n`;
    text += `   β1     : 등가 사각형 응력 블록의 깊이계수(2β)        = ${formatNumber(calc.beta1, 4)}\n\n`;

    text += '3) 철근 재료상수\n';
    text += `   fyd    : 설계인장강도 ( Φs fy )                      = ${formatNumber(calc.fyd, 2)} MPa\n`;
    text += `   εyd    : 설계 항복 변형률 ( fyd / Es )               = ${formatNumber(calc.epsyd, 6)}\n\n`;

    text += '4) 필요철근량 산정\n';
    text += '   Mu = As x fyd x (d - a / 2)              ----------------   ①\n';
    text += '    a = As x fyd / ( η x fcd x b)          ----------------   ②\n';
    text += '   식②를 식①에 대입하여 이차방정식으로 As를 구한다\n';
    text += '         fyd²\n';
    text += `   ─────────────── As² - fyd x d x As + Mu = 0 ,   Asreq = ${formatNumber(calc.Asreq, 1)} mm²\n`;
    text += '    2 x η x fcd x b\n\n';

    const ratio = calc.Asuse / calc.Asreq;
    text += `5) 사용철근량 : Asuse = ${formatNumber(calc.Asuse, 1)} mm², 철근도심 : dc = ${formatNumber(calc.Dc, 1)} mm [ 사용율 = ${formatNumber(ratio, 3)} ]\n`;
    text += `      1단 : ${calc.rebarid}${formatInt(calc.AsDia1)} - ${formatInt(calc.AsNum1)} EA (= ${formatNumber(calc.Asuse1 * calc.AsNum1, 1)} mm², dc1 = ${formatNumber(calc.Dc1, 1)} mm)\n`;
    text += `      2단 : ${calc.rebarid}${formatInt(calc.AsDia2)} - ${formatInt(calc.AsNum2)} EA (= ${formatNumber(calc.Asuse2 * calc.AsNum2, 1)} mm², dc2 = ${formatNumber(calc.Dc2, 1)} mm)\n`;
    text += `      3단 : ${calc.rebarid}${formatInt(calc.AsDia3)} - ${formatInt(calc.AsNum3)} EA (= ${formatNumber(calc.Asuse3 * calc.AsNum3, 1)} mm², dc3 = ${formatNumber(calc.Dc3, 1)} mm)\n\n`;

    text += '6) 철근량 검토\n';
    text += `   As,min = (0.25 √fck / fy) x b x d = ${formatNumber(calc.Asmin1, 1)} mm²\n`;
    text += `          = (1.4 / fy) x b x d = ${formatNumber(calc.Asmin2, 1)} mm²\n`;
    text += `          = As_req x 4 / 3 = ${formatNumber(calc.Asmin3, 1)} mm²\n`;

    if (calc.Asuse >= calc.Asmin) {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² ≥ As,min = ${formatNumber(calc.Asmin, 1)} mm²  ∴ O.K\n`;
    } else {
        text += `   As,use = ${formatNumber(calc.Asuse, 1)} mm² < As,min = ${formatNumber(calc.Asmin, 1)} mm²  ∴ N.G\n`;
    }

    if (calc.Asuse <= calc.Asmax) {
        text += `   As,max = 0.04 x b x d = ${formatNumber(calc.Asmax, 1)} mm² ≥ As,use = ${formatNumber(calc.Asuse, 1)} mm²  ∴ O.K\n\n`;
    } else {
        text += `   As,max = 0.04 x b x d = ${formatNumber(calc.Asmax, 1)} mm² < As,use = ${formatNumber(calc.Asuse, 1)} mm²  ∴ N.G\n\n`;
    }

    text += '7) 중립축 깊이 검토\n';
    text += '   Cmax = (δ x εcu / 0.0033 - 0.6) x d\n';
    text += `        = (${formatNumber(calc.delta, 1)} x ${formatNumber(calc.epscu, 5)} / 0.0033 - 0.6) x ${formatNumber(calc.D, 1)} = ${formatNumber(calc.c_max, 1)} mm\n`;
    text += '   C = Φs x As x fy / (α x Φc x 0.85 x fck x b)\n';
    text += `     = ${formatNumber(calc.Os, 2)} x ${formatNumber(calc.Asuse, 1)} x ${formatInt(calc.fy)} / (${formatNumber(calc.alpha, 2)} x ${formatNumber(calc.Oc, 2)} x 0.85 x ${formatInt(calc.fck)} x ${formatNumber(calc.B, 1)})\n`;

    if (calc.cc <= calc.c_max) {
        text += `     = ${formatNumber(calc.cc, 1)} mm < Cmax = ${formatNumber(calc.c_max, 1)} mm  ∴ O.K\n\n`;
    } else {
        text += `     = ${formatNumber(calc.cc, 1)} mm ≥ Cmax = ${formatNumber(calc.c_max, 1)} mm  ∴ N.G\n\n`;
    }

    text += '8) 인장철근 변형률\n';
    text += '   εs = (d - C) / C x εcu\n';
    text += `      = (${formatNumber(calc.D, 1)} - ${formatNumber(calc.cc, 1)}) / ${formatNumber(calc.cc, 1)} x ${formatNumber(calc.epscu, 5)} = ${formatNumber(calc.epss, 5)}\n`;
    text += '   εyd = Φs x fy / Es\n';

    if (calc.epsyd <= calc.epss) {
        text += `       = ${formatNumber(calc.Os, 2)} x ${formatInt(calc.fy)} / ${formatInt(calc.Es)} = ${formatNumber(calc.epsyd, 5)}  ≤ εs  ∴ 항복가정 O.K\n\n`;
    } else {
        text += `       = ${formatNumber(calc.Os, 2)} x ${formatInt(calc.fy)} / ${formatInt(calc.Es)} = ${formatNumber(calc.epsyd, 5)}  > εs  ∴ 항복가정 N.G\n\n`;
    }

    text += '9) 설계 휨강도 산정\n';
    text += '   Mr = As x Φs x fy x (d - β x c)\n';
    text += `      = ${formatNumber(calc.Asuse, 1)} x ${formatNumber(calc.Os, 2)} x ${formatInt(calc.fy)} x (${formatNumber(calc.D, 1)} - ${formatNumber(calc.beta, 2)} x ${formatNumber(calc.cc, 1)})\n`;

    if (calc.Mr > calc.Mun) {
        text += `      = ${formatNumber(calc.Mr, 1)} N.mm  ≥ Mu = ${formatNumber(calc.Mun, 1)} N.mm  ∴ O.K  [S.F = ${formatNumber(calc.Msf, 3)}]\n`;
    } else {
        text += `      = ${formatNumber(calc.Mr, 1)} N.mm  < Mu = ${formatNumber(calc.Mun, 1)} N.mm  ∴ N.G  [S.F = ${formatNumber(calc.Msf, 3)}]\n`;
    }

    return text;
}

function getShearText(calc) {
    let text = '';

    text += '=' .repeat(70) + '\n';
    text += '                    전단력 검토\n';
    text += '=' .repeat(70) + '\n\n';

    text += '10) 전단검토\n';
    text += '    Vcd = [0.85 x Φc x k x (ρ x fck)^(1/3) + 0.15 x fn] x b x d\n';
    text += `        = [0.85 x ${formatNumber(calc.Oc, 2)} x ${formatNumber(calc.k, 3)} x (${formatNumber(calc.rhos, 6)} x ${formatNumber(calc.fck, 1)})^(1/3) + 0.15 x ${formatNumber(calc.fn, 3)}] x ${formatNumber(calc.B, 1)} x ${formatNumber(calc.D, 1)}\n`;
    text += `        = ${formatNumber(calc.Vc, 0)} N\n`;
    text += `       k = 1 + √(200 / d) = 1 + √(200 / ${formatNumber(calc.D, 1)}) = ${formatNumber(calc.k, 3)} (≤ 2.000)\n`;
    text += `       ρ = As / (b x d) = ${formatNumber(calc.Asuse, 1)} / (${formatNumber(calc.B, 1)} x ${formatNumber(calc.D, 1)}) = ${formatNumber(calc.rho, 6)} ≤ 0.0200\n`;
    text += `       fn = Nu / Ac = ${formatNumber(calc.fnn, 3)} MPa (≤ 0.2 Φc fck = ${formatNumber(calc.fnmax, 3)} MPa, 압축의경우+)\n`;
    text += '    Vcd,min = (0.4 x Φc x fctk + 0.15 x fn] x b x d\n';
    text += `            = (0.4 x ${formatNumber(calc.Oc, 2)} x ${formatNumber(calc.fctk, 3)} + 0.15 x ${formatNumber(calc.fn, 3)}] x ${formatNumber(calc.B, 1)} x ${formatNumber(calc.D, 1)}\n`;
    text += `            = ${formatNumber(calc.Vcdmin, 0)} N\n\n`;

    if (calc.Vcd >= calc.Vun) {
        text += `    Vcd = ${formatNumber(calc.Vcd, 0)} N ≥ Vu = ${formatNumber(calc.Vun, 0)} N  ∴ 전단보강 불필요\n\n`;

        text += '11) 최소 전단철근량 검토\n';
        text += `    Av,use = ${formatNumber(calc.Avs, 1)} mm² ( ${calc.rebarid}${formatInt(calc.AvDia)} - ${formatNumber(calc.AvLeg, 0)}ea, C.T.C = ${formatNumber(calc.AvSpace, 1)} mm )\n`;
        text += `    ρv,min = (0.08 x √fck) / fvy = (0.08 x √${formatNumber(calc.fck, 1)}) / ${formatNumber(calc.fy, 1)} = ${formatNumber(calc.rhovmin, 6)}\n`;

        if (calc.rhovuse >= calc.rhovmin) {
            text += `    ρv,use = ${formatNumber(calc.Avs, 1)} / (${formatNumber(calc.AvSpace, 1)} x ${formatNumber(calc.B, 1)} x sin${formatNumber(calc.alphav, 1)}) = ${formatNumber(calc.rhovuse, 6)} ≥ ${formatNumber(calc.rhovmin, 6)} ∴ O.K\n`;
        } else {
            text += `    ρv,use = ${formatNumber(calc.Avs, 1)} / (${formatNumber(calc.AvSpace, 1)} x ${formatNumber(calc.B, 1)} x sin${formatNumber(calc.alphav, 1)}) = ${formatNumber(calc.rhovuse, 6)} < ${formatNumber(calc.rhovmin, 6)} ∴ N.G\n`;
        }
    } else {
        text += `    Vcd = ${formatNumber(calc.Vcd, 0)} N < Vu = ${formatNumber(calc.Vun, 0)} N  ∴ 전단보강 필요\n\n`;

        text += '11) 전단보강철근 검토\n';
        text += `    θ = ${formatNumber(calc.theta, 1)}°, cotθ = ${formatNumber(calc.cotTheta, 3)}\n`;
        text += `    Av,use = ${formatNumber(calc.Avs, 1)} mm² ( ${calc.rebarid}${formatInt(calc.AvDia)} - ${formatNumber(calc.AvLeg, 0)}ea, C.T.C = ${formatNumber(calc.AvSpace, 1)} mm )\n`;
        text += '    Vd = (Φs x fy x Avs x 0.9 x d / s) x cotθ\n';
        text += `       = (${formatNumber(calc.Os, 2)} x ${formatInt(calc.fy)} x ${formatNumber(calc.Avs, 1)} x 0.9 x ${formatNumber(calc.D, 1)} / ${formatNumber(calc.AvSpace, 1)}) x ${formatNumber(calc.cotTheta, 3)}\n`;
        text += `       = ${formatNumber(calc.Vd, 0)} N\n\n`;

        text += `    Vd,max = (ν x Φc x fck x b x z) / (cotθ + tanθ)\n`;
        text += `           = (${formatNumber(calc.nu, 3)} x ${formatNumber(calc.Oc, 2)} x ${formatInt(calc.fck)} x ${formatNumber(calc.B, 1)} x ${formatNumber(calc.z, 1)}) / (${formatNumber(calc.cotTheta, 3)} + ${formatNumber(calc.tanTheta, 3)})\n`;
        text += `           = ${formatNumber(calc.Vdmax, 0)} N\n\n`;

        const Vtotal = calc.Vcd + calc.Vd;
        if (Vtotal >= calc.Vun) {
            text += `    Vcd + Vd = ${formatNumber(calc.Vcd, 0)} + ${formatNumber(calc.Vd, 0)} = ${formatNumber(Vtotal, 0)} N ≥ Vu = ${formatNumber(calc.Vun, 0)} N  ∴ O.K\n`;
        } else {
            text += `    Vcd + Vd = ${formatNumber(calc.Vcd, 0)} + ${formatNumber(calc.Vd, 0)} = ${formatNumber(Vtotal, 0)} N < Vu = ${formatNumber(calc.Vun, 0)} N  ∴ N.G\n`;
        }
    }

    return text;
}

function getServiceText(calc) {
    let text = '';

    text += '=' .repeat(70) + '\n';
    text += '                    사용성 검토 (균열검토)\n';
    text += '=' .repeat(70) + '\n\n';

    text += '12) 사용성 검토\n';
    text += `    n = Es / Ec = ${formatInt(calc.Es)} / ${formatNumber(calc.Ec, 2)} = ${formatInt(calc.nr)}\n`;
    text += `    Xo = ${formatNumber(calc.Xo, 2)} mm\n`;
    text += `    Io = ${formatNumber(calc.Io, 0)} mm⁴\n\n`;

    text += '    콘크리트 인장응력\n';
    text += `    fct,1 = Ms1 / Io x (H - Xo) = ${formatNumber(calc.fct1, 3)} MPa\n`;
    text += `    fct,5 = Ms5 / Io x (H - Xo) = ${formatNumber(calc.fct5, 3)} MPa\n\n`;

    text += '    철근응력\n';
    text += `    fs,1 = ${formatNumber(calc.fs1, 2)} MPa\n`;
    text += `    fs,5 = ${formatNumber(calc.fs5, 2)} MPa\n\n`;

    text += '    허용응력\n';
    text += `    fca,1 = 0.6 x fck = ${formatNumber(calc.fca1, 2)} MPa (하중조합-1)\n`;
    text += `    fca,5 = 0.45 x fck = ${formatNumber(calc.fca5, 2)} MPa (하중조합-5)\n`;
    text += `    fsa,1 = 0.8 x fy = ${formatNumber(calc.fsa1, 2)} MPa\n\n`;

    text += '13) 간접균열검토\n';
    text += `    철근직경에 의한 허용응력 fsad = ${formatNumber(calc.fsad, 0)} MPa\n`;
    text += `    철근간격에 의한 허용응력 fsas = ${formatNumber(calc.fsas, 0)} MPa\n`;
    text += `    fsa = max(fsad, fsas) = ${formatNumber(calc.fsaf, 0)} MPa\n\n`;

    text += '14) 최소철근량 검토\n';
    text += `    Act = B x (H - Xo) = ${formatNumber(calc.B, 1)} x (${formatNumber(calc.H, 1)} - ${formatNumber(calc.Xo, 2)}) = ${formatNumber(calc.Act, 1)} mm²\n`;
    text += `    kc = ${formatNumber(calc.kc, 4)}\n`;
    text += `    k = ${formatNumber(calc.k_crack, 4)}\n`;
    text += `    As,min = kc x k x Act x fct / fsa = ${formatNumber(calc.Asdmin, 1)} mm²\n\n`;

    if (calc.Asuse >= calc.Asdmin) {
        text += `    As,use = ${formatNumber(calc.Asuse, 1)} mm² ≥ As,min = ${formatNumber(calc.Asdmin, 1)} mm²  ∴ O.K\n`;
    } else {
        text += `    As,use = ${formatNumber(calc.Asuse, 1)} mm² < As,min = ${formatNumber(calc.Asdmin, 1)} mm²  ∴ N.G\n`;
    }

    return text;
}

function getFullCalcText(calc) {
    let text = '';

    text += '╔' + '═'.repeat(68) + '╗\n';
    text += '║' + '                    RC 단면 검토 계산서                              ' + '║\n';
    text += '╚' + '═'.repeat(68) + '╝\n\n';

    text += getMomentText(calc);
    text += '\n';
    text += getShearText(calc);
    text += '\n';
    text += getServiceText(calc);

    return text;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { getMomentText, getShearText, getServiceText, getFullCalcText };
}
