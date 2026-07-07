/**
 * RC Section Calculator - 강도설계법 (USD)
 * 직사각형 단철근보 단면검토 (도로교설계기준 강도설계법, 2010)
 *
 * 한계상태설계법(SecBack)과 동일한 datalist 인터페이스를 사용하되,
 * 재료계수(Øc, Øs) 대신 강도감소계수 φ(휨, 전단)를 사용한다.
 *
 * 주요 가정:
 *   - 콘크리트 극한변형률 εcu = 0.003
 *   - 등가직사각형 응력블록 계수 β1 : fck ≤ 28 → 0.85,
 *     fck > 28 → 0.85 - 0.007(fck-28) ≥ 0.65
 *   - 콘크리트 탄성계수 Ec = 8500·∛(fck+8)
 *   - φf(휨, 인장지배) 기본 0.85, φv(전단·비틀림) 기본 0.80
 */

class SecBackUSD {
    constructor(datalist, datalist1, datalist2, datalist3, datalist4, datalist5) {
        // datalist:  [fck, fy]
        // datalist1: [φf, φv]  (강도감소계수: 휨, 전단)
        // datalist2: [H, B]
        // datalist3: 휨철근 정보 [dia,num,dc, dia,num,dc, dia,num,dc]
        // datalist4: 전단철근 정보 [dia,leg,s, sg, seta, αv]
        // datalist5: 부재력 정보 [Mu, Vu, Nu, Ms-1, Ms-5, method]

        this.fck = datalist[0];
        this.fy = datalist[1];
        this.phif = datalist1[0];         // 휨 강도감소계수 φ
        this.phiv = datalist1[1];         // 전단 강도감소계수 φ
        this.H = datalist2[0];
        this.B = datalist2[1];
        this.AsDia1 = datalist3[0];
        this.AsNum1 = datalist3[1];
        this.Dc1 = datalist3[2];
        this.AsDia2 = datalist3[3];
        this.AsNum2 = datalist3[4];
        this.Dc2 = datalist3[5];
        this.AsDia3 = datalist3[6];
        this.AsNum3 = datalist3[7];
        this.Dc3 = datalist3[8];
        this.AvDia = datalist4[0];
        this.AvLeg = datalist4[1];
        this.AvSpace = datalist4[2];
        this.alphav = datalist4[5];
        this.Mu = datalist5[0];
        this.Vu = datalist5[1];
        this.Nu = datalist5[2];
        this.Ms1 = datalist5[3];
        this.Ms5 = datalist5[4];

        this.Es = 200000;                 // 철근의 탄성계수
        this.epscu = 0.003;               // 강도설계법 극한변형률
        this.Mun = this.Mu * 1000000;
        this.Vun = this.Vu * 1000;
        this.Nun = this.Nu * 1000;
        this.Msn1 = this.Ms1 * 1000000;
        this.Msn5 = this.Ms5 * 1000000;

        this.rebarid = this.fy <= 300 ? "D" : "H";

        // 등가직사각형 응력블록 깊이계수 β1
        if (this.fck <= 28) {
            this.beta1 = 0.85;
        } else {
            this.beta1 = Math.max(0.85 - 0.007 * (this.fck - 28), 0.65);
        }

        // 콘크리트 탄성계수 Ec = 8500·∛(fcu), fcu = fck + 8
        this.fcu = this.fck + 8;
        this.Ec = 8500 * Math.pow(this.fcu, 1 / 3);

        // 철근 단면적
        this.Asuse1 = this.rebar(this.AsDia1);
        this.Asuse2 = this.rebar(this.AsDia2);
        this.Asuse3 = this.rebar(this.AsDia3);

        this.Asspace1 = this.AsNum1 === 0 ? 0 : this.B / this.AsNum1;
        this.Asspace2 = this.AsNum2 === 0 ? 0 : this.B / this.AsNum2;
        this.Asspace3 = this.AsNum3 === 0 ? 0 : this.B / this.AsNum3;

        const totalAs = this.Asuse1 * this.AsNum1 + this.Asuse2 * this.AsNum2 + this.Asuse3 * this.AsNum3;
        if (totalAs > 0) {
            this.Dc = (this.Asuse1 * this.AsNum1 * this.Dc1 +
                       this.Asuse2 * this.AsNum2 * this.Dc2 +
                       this.Asuse3 * this.AsNum3 * this.Dc3) / totalAs;
        } else {
            this.Dc = this.Dc1;
        }

        this.D = this.H - this.Dc;        // 단면 유효높이
    }

    rebar(AsDia) {
        const ubarea = [71.30, 126.70, 198.60, 286.50, 387.10, 506.70, 642.40, 794.20, 956.6];
        const dias = [10, 13, 16, 19, 22, 25, 29, 32, 35];
        const index = dias.indexOf(AsDia);
        return index >= 0 ? ubarea[index] : 0;
    }

    // 휨모멘트 검토
    calmoment() {
        this.Asuse = this.Asuse1 * this.AsNum1 + this.Asuse2 * this.AsNum2 + this.Asuse3 * this.AsNum3;
        this.rho = this.D > 0 ? this.Asuse / (this.B * this.D) : 0;

        // 필요철근량 산정 : Mu/φ = As·fy·(d - a/2), a = As·fy/(0.85·fck·b)
        const ta = Math.pow(this.fy, 2) / (2 * 0.85 * this.fck * this.B);
        const tb = -this.fy * this.D;
        const tc = this.Mun / this.phif;
        const disc = tb * tb - 4 * ta * tc;
        this.Asreq = disc >= 0 ? (-tb - Math.sqrt(disc)) / (2 * ta) : NaN;

        // 최소철근량
        this.Asmin1 = 0.25 * Math.sqrt(this.fck) * this.B * this.D / this.fy;
        this.Asmin2 = 1.4 * this.B * this.D / this.fy;
        this.Asmin = Math.max(this.Asmin1, this.Asmin2);

        // 균형철근비 및 최대철근량 (ρmax = 0.75·ρb)
        this.rhob = 0.85 * this.beta1 * (this.fck / this.fy) * (600 / (600 + this.fy));
        this.rhomax = 0.75 * this.rhob;
        this.Asmax = this.rhomax * this.B * this.D;

        // 설계 휨강도
        this.a = this.Asuse * this.fy / (0.85 * this.fck * this.B);   // 등가응력블록 깊이
        this.cc = this.a / this.beta1;                                // 중립축 깊이
        this.Mn = this.Asuse * this.fy * (this.D - this.a / 2);       // 공칭휨강도
        this.Mr = this.phif * this.Mn;                                // 설계휨강도 φMn
        this.Msf = this.Mun !== 0 ? this.Mr / this.Mun : 0;

        // 인장철근 변형률 (연성 검토)
        this.epst = this.cc > 0 ? (this.D - this.cc) / this.cc * this.epscu : 0; // 순인장변형률
        this.epsy = this.fy / this.Es;                                // 항복변형률
    }

    // 전단력 검토
    calshear() {
        this.Ag = this.B * this.H;

        // 콘크리트가 부담하는 전단강도 Vc (축력 영향 반영)
        if (this.Nun >= 0) {
            this.axialFactor = 1 + this.Nun / (14 * this.Ag);        // 압축 : 증가
        } else {
            this.axialFactor = Math.max(0, 1 + this.Nun / (3.5 * this.Ag)); // 인장 : 감소
        }
        this.Vc = (1 / 6) * this.axialFactor * Math.sqrt(this.fck) * this.B * this.D;
        this.Vc = Math.max(this.Vc, 0);

        // 전단철근이 부담하는 전단강도 Vs
        this.Avs = this.rebar(this.AvDia) * this.AvLeg;
        this.Vs = this.AvSpace > 0 ? this.Avs * this.fy * this.D / this.AvSpace : 0;
        this.Vsmax = (2 / 3) * Math.sqrt(this.fck) * this.B * this.D;   // Vs 상한

        this.Vn = this.Vc + this.Vs;
        this.Vr = this.phiv * this.Vn;                                  // 설계전단강도 φVn
        this.phiVc = this.phiv * this.Vc;

        // 최소전단철근량 (ρv,min)
        this.rhovmin = Math.max(0.0625 * Math.sqrt(this.fck) / this.fy, 0.35 / this.fy);
        this.rhovuse = this.AvSpace > 0 ? this.Avs / (this.AvSpace * this.B) : 0;

        // 전단철근 간격 제한
        const Vscheck = (1 / 3) * Math.sqrt(this.fck) * this.B * this.D;
        if (this.Vs <= Vscheck) {
            this.smax = Math.min(this.D / 2, 600);
        } else {
            this.smax = Math.min(this.D / 4, 300);
        }

        // 전단설계 판정 구분
        //   Vu ≤ φVc/2         : 전단철근 불필요
        //   φVc/2 < Vu ≤ φVc   : 최소전단철근
        //   Vu > φVc           : 전단보강 필요
        if (this.Vun <= this.phiVc / 2) {
            this.shearCase = 'none';
        } else if (this.Vun <= this.phiVc) {
            this.shearCase = 'min';
        } else {
            this.shearCase = 'reinf';
        }
    }

    // 사용성 검토 (균열검토, 탄성 균열단면)
    calservice() {
        this.nr = Math.round(this.Es / this.Ec);      // 탄성계수비 n

        // 균열모멘트 (파괴계수 fr = 0.63√fck)
        this.fr = 0.63 * Math.sqrt(this.fck);
        this.Ig = this.B * Math.pow(this.H, 3) / 12;
        this.yt = this.H / 2;
        this.Mcr = this.fr * this.Ig / this.yt;

        // 균열단면 중립축 : b·x²/2 = n·As·(d - x)
        const nA = this.nr * this.Asuse;
        if (this.B > 0 && nA > 0) {
            this.xcr = (-nA + Math.sqrt(nA * nA + 2 * this.B * nA * this.D)) / this.B;
        } else {
            this.xcr = 0;
        }
        this.Icr = this.B * Math.pow(this.xcr, 3) / 3 + nA * Math.pow(this.D - this.xcr, 2);

        // 사용하중 상태의 철근/콘크리트 응력
        if (this.Icr > 0) {
            this.fs1 = this.nr * this.Msn1 * (this.D - this.xcr) / this.Icr;
            this.fs5 = this.nr * this.Msn5 * (this.D - this.xcr) / this.Icr;
            this.fc1 = this.Msn1 * this.xcr / this.Icr;
            this.fc5 = this.Msn5 * this.xcr / this.Icr;
        } else {
            this.fs1 = this.fs5 = this.fc1 = this.fc5 = 0;
        }

        // 허용응력
        this.fca = 0.6 * this.fck;    // 콘크리트 허용압축응력
        this.fsa = 0.8 * this.fy;     // 철근 허용인장응력 (참고값)

        // 간접균열검토 (철근직경/간격에 의한 허용응력)
        const crdia = [32, 25, 16, 14, 10, 8];
        const crspace = [300, 250, 200, 150, 100, 50];
        const index = [160, 200, 240, 280, 320, 360];

        if (this.AsDia1 <= crdia[5]) this.fsad = index[5];
        else if (this.AsDia1 <= crdia[4]) this.fsad = index[4];
        else if (this.AsDia1 <= crdia[3]) this.fsad = index[3];
        else if (this.AsDia1 <= crdia[2]) this.fsad = index[2];
        else if (this.AsDia1 <= crdia[1]) this.fsad = index[1];
        else this.fsad = index[0];

        if (this.Asspace1 <= crspace[5]) this.fsas = index[5];
        else if (this.Asspace1 <= crspace[4]) this.fsas = index[4];
        else if (this.Asspace1 <= crspace[3]) this.fsas = index[3];
        else if (this.Asspace1 <= crspace[2]) this.fsas = index[2];
        else if (this.Asspace1 <= crspace[1]) this.fsas = index[1];
        else this.fsas = index[0];

        this.fsaf = Math.max(this.fsad, this.fsas);
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SecBackUSD;
}
