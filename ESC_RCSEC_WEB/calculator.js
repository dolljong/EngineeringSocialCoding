/**
 * RC Section Calculator
 * 직사각형 단철근보 단면검토 (도로교설계기준 2012)
 * Converted from Python (sec_back_ver031.py)
 */

class SecBack {
    constructor(datalist, datalist1, datalist2, datalist3, datalist4, datalist5) {
        // datalist: [fck, fy]
        // datalist1: [Øc, Øs]
        // datalist2: [H, B]
        // datalist3: 휨철근 정보 [dia,num,dc, dia,num,dc, dia,num,dc]
        // datalist4: 전단철근 정보 [dia,num,s,sg,seta,αv]
        // datalist5: 부재력 정보 [Mu, Vu, Nu, Ms-1, Ms-5, method]

        this.fck = datalist[0];           // fck설정
        this.fy = datalist[1];            // fy설정
        this.Oc = datalist1[0];           // Øc설정
        this.Os = datalist1[1];           // Øs설정
        this.H = datalist2[0];            // 단면두께 설정
        this.B = datalist2[1];            // 단면 폭 설정
        this.AsDia1 = datalist3[0];       // 1단 철근직경 설정
        this.AsNum1 = datalist3[1];       // 1단 철근개수 설정
        this.Dc1 = datalist3[2];          // 1단 피복두께 설정
        this.AsDia2 = datalist3[3];       // 2단 철근직경 설정
        this.AsNum2 = datalist3[4];       // 2단 철근개수 설정
        this.Dc2 = datalist3[5];          // 2단 피복두께 설정
        this.AsDia3 = datalist3[6];       // 3단 철근직경 설정
        this.AsNum3 = datalist3[7];       // 3단 철근개수 설정
        this.Dc3 = datalist3[8];          // 3단 피복두께 설정
        this.AvDia = datalist4[0];        // 전단철근 직경
        this.AvLeg = datalist4[1];        // 전단철근 다리개수
        this.AvSpace = datalist4[2];      // 전단철근 배치간격
        this.sg = datalist4[3];           // 복부스트럿 각도 입력방법 선택
        this.seta = datalist4[4];         // 복부스트럿 각도 직접입력값
        this.alphav = datalist4[5];       // 전단철근과 주철근 각도
        this.Mu = datalist5[0];           // Mu설정
        this.Vu = datalist5[1];           // Vu설정
        this.Nu = datalist5[2];           // Nu설정
        this.Ms1 = datalist5[3];          // Ms-1설정
        this.Ms5 = datalist5[4];          // Ms-5설정
        this.crid = datalist5[5];         // 사용성검토방법 설정
        this.delta = 1;                   // 재분배 모멘트율 설정
        this.Es = 200000;                 // 철근의 탄성계수
        this.Mun = this.Mu * 1000000;
        this.Vun = this.Vu * 1000;
        this.Nun = this.Nu * 1000;
        this.Msn1 = this.Ms1 * 1000000;
        this.Msn5 = this.Ms5 * 1000000;
        this.alphacc = 0.85;              // 유효계수

        if (this.fy <= 300) {
            this.rebarid = "D";
        } else {
            this.rebarid = "H";
        }

        this.fcd = this.fck * this.Oc * this.alphacc; // 콘크리트 설계압축강도

        // 콘크리트 평균압축강도
        if (this.fck < 40) {
            this.fcm = this.fck + 4;
        } else if (this.fck >= 60) {
            this.fcm = this.fck + 6;
        } else {
            this.fcm = 4 + (this.fck - 40) / 10;
        }

        this.Ec = 0.077 * Math.pow(2500, 1.5) * Math.pow(this.fcm, 1/3); // 콘크리트 탄성계수

        // 상승곡선부의 형상을 나타내는 지수
        const neps_calc = 1.2 + 1.5 * Math.pow((100 - this.fck) / 60, 4);
        this.neps = neps_calc >= 2 ? 2 : neps_calc;

        // 최대응력에 처음 도달했을때의 변형률
        const epsco_calc = 0.002 + ((this.fck - 40) / 100000);
        this.epsco = epsco_calc <= 0.002 ? 0.002 : epsco_calc;

        // 콘크리트 극한변형율
        const epscu_calc = 0.0033 - ((this.fck - 40) / 100000);
        this.epscu = epscu_calc >= 0.0033 ? 0.0033 : epscu_calc;

        // 보간 테이블
        const fcklist = [40, 50, 60, 70, 80, 90];
        const alpalist = [0.8, 0.78, 0.72, 0.67, 0.63, 0.59];
        const betalist = [0.4, 0.4, 0.38, 0.37, 0.36, 0.35];
        const etalist = [1.0, 0.97, 0.95, 0.91, 0.87, 0.84];

        // 압축합력의 응력계수 α
        if (this.fck <= 40) {
            this.alpha = alpalist[0];
        } else if (this.fck >= 90) {
            this.alpha = alpalist[5];
        } else {
            this.alpha = this.interpolate(fcklist, alpalist, this.fck);
        }

        // 압축합력의 작용점 위치계수 β
        if (this.fck <= 40) {
            this.beta = betalist[0];
        } else if (this.fck >= 90) {
            this.beta = betalist[5];
        } else {
            this.beta = this.interpolate(fcklist, betalist, this.fck);
        }

        // 등가사각형 응력블록의 크기계수 η
        if (this.fck <= 40) {
            this.eta = etalist[0];
        } else if (this.fck >= 90) {
            this.eta = etalist[5];
        } else {
            this.eta = this.interpolate(fcklist, etalist, this.fck);
        }

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

        this.D = this.H - this.Dc;  // 단면 유효높이
        this.beta1 = this.beta * 2; // 등가사각형 응력블록의 깊이계수
    }

    interpolate(xList, yList, x) {
        for (let i = 0; i < xList.length - 1; i++) {
            if (x >= xList[i] && x <= xList[i + 1]) {
                const t = (x - xList[i]) / (xList[i + 1] - xList[i]);
                return yList[i] + t * (yList[i + 1] - yList[i]);
            }
        }
        return yList[0];
    }

    rebar(AsDia) {
        const ubarea = [71.30, 126.70, 198.60, 286.50, 387.10, 506.70, 642.40, 794.20, 956.6];
        const dias = [10, 13, 16, 19, 22, 25, 29, 32, 35];
        const index = dias.indexOf(AsDia);
        return index >= 0 ? ubarea[index] : 0;
    }

    // 휨모멘트 검토
    calmoment() {
        this.pmin = Math.max(0.25 * Math.sqrt(this.fck) / this.fy, 1.4 / this.fy); // 최소철근비

        this.Asuse = this.Asuse1 * this.AsNum1 + this.Asuse2 * this.AsNum2 + this.Asuse3 * this.AsNum3; // 전체 사용철근량
        this.rho = this.Asuse / (this.B * this.D); // 사용철근비
        this.fyd = this.fy * this.Os; // 철근 설계인장강도
        this.epsyd = this.fyd / this.Es;

        const ta = Math.pow(this.fyd, 2) / (2 * this.eta * this.fcd * this.B);
        const tb = -this.fyd * this.D;
        this.Asreq = (-tb - Math.sqrt(tb * tb - 4 * ta * this.Mun)) / (2 * ta); // 필요철근량 산정

        this.Asmin1 = 0.25 * Math.sqrt(this.fck) * this.B * this.D / this.fy;
        this.Asmin2 = 1.4 * this.B * this.D / this.fy;
        this.Asmin3 = 4 * this.Asreq / 3;
        this.Asmin = Math.min(Math.max(this.Asmin1, this.Asmin2), this.Asmin3);
        this.Asmax = 0.04 * this.B * this.D;

        this.c_max = (this.delta * this.epscu / 0.0033 - 0.6) * this.D;

        this.cc = (this.Asuse * this.Os * this.fy) / (this.alpha * this.Oc * 0.85 * this.fck * this.B);

        this.epsyd = this.Os * this.fy / this.Es;
        this.epss = (this.D - this.cc) / this.cc * this.epscu;

        this.Mr = this.Asuse * this.Os * this.fy * (this.D - this.beta * this.cc);

        this.Msf = this.Mr / this.Mun;
    }

    // 전단력 검토
    calshear() {
        this.k = 1 + Math.sqrt(200 / this.D); // 단면크기효과 고려한 계수
        this.k1 = this.k > 2 ? 2 : this.k;

        this.fctk = 0.7 * 0.3 * Math.pow(this.fcm, 2/3); // 콘크리트 인장강도
        this.fnn = this.Nun / (this.H * this.B); // 전단철근이 없는경우 축인장응력
        this.fnmax = 0.2 * this.Oc * this.fck;
        this.fn = Math.min(this.fnn, this.fnmax);
        this.rhos = Math.min(this.rho, 0.02);

        this.Vc = (0.85 * this.Oc * this.k * Math.pow(this.rhos * this.fck, 1/3) + 0.15 * this.fn) * (this.B * this.D);
        this.Vcdmin = (0.4 * this.Oc * this.fctk + 0.15 * this.fn) * (this.B * this.D);
        this.Vcd = Math.max(this.Vc, this.Vcdmin);

        this.Avs = this.rebar(this.AvDia) * this.AvLeg; // 전단철근량
        this.alphaShear = 90.0;
        this.nu = 0.6 * (1 - this.fck / 250);
        this.z = 0.9 * this.D;

        // αcw 계산
        if (this.fnn < 0) {
            this.alphacw = 0;
        } else if (this.fnn === 0) {
            this.alphacw = 1.0;
        } else if (this.fnn <= 0.25 * this.Oc * this.fck) {
            this.alphacw = 1.0 + this.fnn / (this.Oc * this.fck);
        } else if (this.fnn <= 0.5 * this.Oc * this.fck) {
            this.alphacw = 1.25;
        } else if (this.fnn <= 1.0 * this.Oc * this.fck) {
            this.alphacw = 2.5 * (1 - this.fnn / (this.Oc * this.fck));
        } else {
            this.alphacw = 0;
        }

        this.cotTheta1 = 2.5; // cotθ = 2.5(θ=21.8도) 적용시
        this.tanTheta1 = 1 / this.cotTheta1;
        this.cotTheta2 = 1; // cotθ = 1.0(θ=45.0도) 적용시
        this.tanTheta2 = 1 / this.cotTheta2;
        this.Vdmax1 = (this.nu * this.Oc * this.fck * this.B * this.z) / (this.cotTheta1 + this.tanTheta1);
        this.Vdmax2 = (this.nu * this.Oc * this.fck * this.B * this.z) / (this.cotTheta2 + this.tanTheta2);

        if (this.sg === 1) {
            this.cotTheta = this.seta;
        } else if (this.sg === 2) {
            this.cotTheta = (1 + 2.5) / 2;
        } else {
            if (this.Vun <= this.Vdmax1) {
                this.cotTheta = 2.5;
            } else if (this.Vun > this.Vdmax2) {
                this.cotTheta = 0;
            } else {
                this.cotTheta = 1 / Math.tan(0.5 * Math.asin(this.Vun / (0.2 * this.fck * (1 - this.fck / 250) * this.B * this.z)));
            }
        }

        this.tanTheta = 1 / this.cotTheta;
        this.theta = Math.atan(this.tanTheta) * 180 / Math.PI;

        this.Vd = (this.Os * this.fy * this.Avs * 0.9 * this.D / this.AvSpace) * this.cotTheta;
        this.Vdmax = (this.nu * this.Oc * this.fck * this.B * this.z) / (this.cotTheta + this.tanTheta);

        this.rhovuse = this.Avs / (this.AvSpace * this.B * Math.sin(this.alphav * Math.PI / 180));
        this.rhovmin = 0.08 * Math.sqrt(this.fck) / this.fy;
        this.s1max = 0.75 * this.D * (1 + (1 / Math.tan(this.alphav * Math.PI / 180)));
        this.s2max = Math.min(0.75 * this.D, 600);
        this.s2 = this.B / this.AvLeg;
        this.dTr = (this.Mr - this.Mun) / this.D;
        this.dT = 0.5 * this.Vun * (this.cotTheta - 1 / Math.tan(this.alphav * Math.PI / 180));
    }

    // 사용성 검토(균열검토)
    calservice() {
        this.nr = Math.round(this.Es / this.Ec); // 철근비 산정(반올림)
        this.Xo = (this.B * this.H * this.H / 2 + (this.nr - 1) * this.Asuse * this.D) /
                  (this.B * this.H + (this.nr - 1) * this.Asuse);
        this.Io = this.B * Math.pow(this.H, 3) / 12 +
                  this.B * this.H * Math.pow(this.H / 2 - this.Xo, 2) +
                  (this.nr - 1) * this.Asuse * Math.pow(this.D - this.Xo, 2);
        this.fct1 = this.Msn1 / this.Io * (this.H - this.Xo);
        this.fct5 = this.Msn5 / this.Io * (this.H - this.Xo);

        this.D1 = this.H - this.Dc1;
        this.c_service = -this.nr * this.rho + Math.sqrt(Math.pow(this.nr * this.rho, 2) + 2 * this.nr * this.rho);
        this.x = this.k * this.D;
        this.fc1 = 2 * this.Msn1 / (this.B * this.x * (this.D - this.x / 3));
        this.fc5 = 2 * this.Msn5 / (this.B * this.x * (this.D - this.x / 3));
        this.fs1 = this.Msn1 / (this.Asuse * (this.D1 - this.x / 3));
        this.fs5 = this.Msn5 / (this.Asuse * (this.D1 - this.x / 3));
        this.fca1 = 0.6 * this.fck;
        this.fca5 = 0.45 * this.fck;
        this.fsa1 = 0.8 * this.fy;

        this.fsa = Math.max(160, 360);
        this.Act = this.B * (this.H - this.Xo);

        // k1 산정
        if (this.Nu >= 0) {
            this.k1_service = 1.5;
        } else {
            const h1 = this.H < 1000 ? this.H : 1000;
            this.k1_service = 2 * h1 / (3 * this.H);
        }

        // 부등분포 반영 계수
        if (this.H <= 300) {
            this.k_crack = 1.0;
        } else if (this.H < 800) {
            this.k_crack = -0.0007 * this.H + 1.21;
        } else {
            this.k_crack = 0.65;
        }

        this.fct = this.fctk / 0.7; // fct = fctm

        // 단면높이의 한계 산정
        this.h1 = this.H <= 1000 ? this.H : 1000;
        this.kc = Math.min(0.4 * (1 - this.fn / (this.k1_service * (this.H / this.h1) * this.fct)), 1);
        this.Asdmin = this.kc * this.k_crack * this.Act * this.fct / this.fsa;

        // 간접균열검토
        const crdia = [32, 25, 16, 14, 10, 8];
        const crspace = [300, 250, 200, 150, 100, 50];
        const index = [160, 200, 240, 280, 320, 360];

        if (this.AsDia1 <= crdia[5]) {
            this.fsad = index[5];
        } else if (this.AsDia1 <= crdia[4]) {
            this.fsad = index[4];
        } else if (this.AsDia1 <= crdia[3]) {
            this.fsad = index[3];
        } else if (this.AsDia1 <= crdia[2]) {
            this.fsad = index[2];
        } else if (this.AsDia1 <= crdia[1]) {
            this.fsad = index[1];
        } else {
            this.fsad = index[0];
        }

        if (this.Asspace1 <= crspace[5]) {
            this.fsas = index[5];
        } else if (this.Asspace1 <= crspace[4]) {
            this.fsas = index[4];
        } else if (this.Asspace1 <= crspace[3]) {
            this.fsas = index[3];
        } else if (this.Asspace1 <= crspace[2]) {
            this.fsas = index[2];
        } else if (this.Asspace1 <= crspace[1]) {
            this.fsas = index[1];
        } else {
            this.fsas = index[0];
        }

        this.fsaf = Math.max(this.fsad, this.fsas);
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SecBack;
}
