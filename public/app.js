
  
  function formatPlayerSquadDisplayName(name) {
    if (!name) return '선수';
    const commonMap = {
      '아리손 람세스 베커': '알리송',
      '클라우디오 안드레 메르겐 타파렐': '타파렐',
      '시아고 실바 시아고 에미리아노 실바': '티아고 실바',
      '아르다이르 나스시멘토 도스 산투스': '알다이르',
      '카를로스 헨리케 카세미로': '카세미루',
      '호베르투 카를루스 다 시우바 호샤': '호베르투 카를루스',
      '다니엘 알베르토 파사렐라': '다니엘 파사렐라',
      '하비에르 아델마르 자네티': '하비에르 자네티',
      '우발도 마틸도 필롤': '우발도 필롤',
      '가브리엘 오마르 바티스투타': '바티스투타',
      '디에고 아르만도 마라도나': '디에고 마라도나',
      '후안 파블로 소린': '후안 파블로 소린',
      '호나우두 루이스 나자리오 데 리마': '호나우두',
      '호나우두 데 아시스 모레이라': '호나우지뉴',
      '에드손 아란테스 도 나시멘토': '펠레',
      '아르투르 안투네스 코임브라': '지쿠',
      '리카르도 이젝손 도스 산토스 레이치': '카카',
      '오스카르 알프레도 루헤리': '오스카르 루헤리'
    };
    if (commonMap[name]) return commonMap[name];
    name = name.split('(')[0].trim();
    const words = name.split(/\s+/);
    if (words.length > 3) {
      const unique = Array.from(new Set(words));
      if (unique.length <= 2) return unique.join(' ');
      return `${unique[0]} ${unique[unique.length - 1]}`;
    }
    return name;
  }

  function getDisplayShortName(name) {
    if (!name) return '선수';
    name = name.split('(')[0].trim();
    const parts = name.split(/\s+/);
    if (parts.length === 1) return name;
    if (parts.length === 2 && name.length <= 8) return name;
    // For long full names, return the last surname or football moniker
    return parts[parts.length - 1];
  }

  function getPositionColor(pos) {
    if (!pos) return 'text-sky-400';
    if (pos.startsWith('GK')) return 'text-amber-400';
    if (pos.includes('B') || pos.includes('DF')) return 'text-sky-400';
    if (pos.includes('M')) return 'text-emerald-400';
    if (pos.includes('W') || pos.includes('ST') || pos.includes('FW')) return 'text-rose-400';
    return 'text-sky-400';
  }

// -*- coding: utf-8 -*-
/**
 * ALL-TIME XI — Interactive Frontend Application
 * Covers:
 * 1. Home & FIFA Top 30 Country Selection (with Live Hero Tactical Pitch)
 * 2. Best 11 Tactical Board Builder (7 Formations, Drag & Drop + Touch Swap, Suitability Engine, PNG Export, Share URL)
 * 3. AI Dream Match Arena (Gemini / OpenAI Server-Side Comparison, 6-Section Report, VS PNG Export, Share URL)
 * 4. Historical Player Database Explorer (3,817 Verified 30+ Caps Players, Era/Position Filters, Source-Backed Detail Modal)
 * 5. Data Quality & Source Verification Dashboard + Hidden Admin Console with Audit Logs
 */

(function () {
  const TACTICAL_STYLES = ['점유율 축구', '강한 전방 압박', '역습', '수비 중심', '균형형'];
  const BOARD_THEMES = [
    { id: 'classic_emerald', name: '클래식 에메랄드 잔디', dark: '#0f522d', light: '#136236', border: 'rgba(255,255,255,0.82)' },
    { id: 'midnight_tactics', name: '미드나잇 데이터 보드', dark: '#0f172a', light: '#172554', border: 'rgba(56,189,248,0.75)' },
    { id: 'worldcup_gold', name: '월드컵 골드 에디션', dark: '#113e26', light: '#164e30', border: 'rgba(250,204,21,0.85)' },
    { id: 'royal_turf', name: '로열 챔피언스 터프', dark: '#0c4a3e', light: '#115e50', border: 'rgba(241,245,249,0.82)' }
  ];

const DEFAULT_FORMATIONS = [
  {
    "code": "4-3-3",
    "name_ko": "4-3-3 (클래식 윙 포워드 & 역삼각형 중원)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LB",
        "label_ko": "좌측 풀백",
        "group": "DF",
        "x": 15,
        "y": 73,
        "compatible": [
          "LB",
          "LWB",
          "CB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 37,
        "y": 75,
        "compatible": [
          "CB",
          "LCB",
          "RCB",
          "CDM"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 63,
        "y": 75,
        "compatible": [
          "CB",
          "RCB",
          "LCB",
          "CDM"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "RB",
        "label_ko": "우측 풀백",
        "group": "DF",
        "x": 85,
        "y": 73,
        "compatible": [
          "RB",
          "RWB",
          "CB"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LCM",
        "label_ko": "좌측 중앙 미드필더",
        "group": "MF",
        "x": 28,
        "y": 48,
        "compatible": [
          "CM",
          "CAM",
          "CDM",
          "LM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "CDM",
        "label_ko": "수비형 미드필더",
        "group": "MF",
        "x": 50,
        "y": 56,
        "compatible": [
          "CDM",
          "CM",
          "CB"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "RCM",
        "label_ko": "우측 중앙 미드필더",
        "group": "MF",
        "x": 72,
        "y": 48,
        "compatible": [
          "CM",
          "CAM",
          "CDM",
          "RM"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "LW",
        "label_ko": "좌측 윙어",
        "group": "FW",
        "x": 18,
        "y": 23,
        "compatible": [
          "LW",
          "LM",
          "ST",
          "CAM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "ST",
        "label_ko": "스트라이커",
        "group": "FW",
        "x": 50,
        "y": 17,
        "compatible": [
          "ST",
          "CF",
          "LW",
          "RW",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "RW",
        "label_ko": "우측 윙어",
        "group": "FW",
        "x": 82,
        "y": 23,
        "compatible": [
          "RW",
          "RM",
          "ST",
          "CAM"
        ]
      }
    ]
  },
  {
    "code": "4-2-3-1",
    "name_ko": "4-2-3-1 (더블 볼란치 & 플레이메이커)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LB",
        "label_ko": "좌측 풀백",
        "group": "DF",
        "x": 15,
        "y": 73,
        "compatible": [
          "LB",
          "LWB",
          "CB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 37,
        "y": 75,
        "compatible": [
          "CB",
          "LCB",
          "RCB",
          "CDM"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 63,
        "y": 75,
        "compatible": [
          "CB",
          "RCB",
          "LCB",
          "CDM"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "RB",
        "label_ko": "우측 풀백",
        "group": "DF",
        "x": 85,
        "y": 73,
        "compatible": [
          "RB",
          "RWB",
          "CB"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LDM",
        "label_ko": "좌측 수비형 미드필더",
        "group": "MF",
        "x": 35,
        "y": 56,
        "compatible": [
          "CDM",
          "CM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "RDM",
        "label_ko": "우측 수비형 미드필더",
        "group": "MF",
        "x": 65,
        "y": 56,
        "compatible": [
          "CDM",
          "CM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "LAM",
        "label_ko": "좌측 공격형 미드필더",
        "group": "MF",
        "x": 20,
        "y": 35,
        "compatible": [
          "LW",
          "CAM",
          "LM",
          "ST"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "CAM",
        "label_ko": "중앙 공격형 미드필더",
        "group": "MF",
        "x": 50,
        "y": 35,
        "compatible": [
          "CAM",
          "CM",
          "ST",
          "LW",
          "RW"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "RAM",
        "label_ko": "우측 공격형 미드필더",
        "group": "MF",
        "x": 80,
        "y": 35,
        "compatible": [
          "RW",
          "CAM",
          "RM",
          "ST"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "ST",
        "label_ko": "스트라이커",
        "group": "FW",
        "x": 50,
        "y": 17,
        "compatible": [
          "ST",
          "CF",
          "LW",
          "RW"
        ]
      }
    ]
  },
  {
    "code": "4-4-2",
    "name_ko": "4-4-2 (클래식 투톱 & 두 줄 수비)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LB",
        "label_ko": "좌측 풀백",
        "group": "DF",
        "x": 15,
        "y": 73,
        "compatible": [
          "LB",
          "LWB",
          "CB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 37,
        "y": 75,
        "compatible": [
          "CB",
          "LCB",
          "RCB",
          "CDM"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 63,
        "y": 75,
        "compatible": [
          "CB",
          "RCB",
          "LCB",
          "CDM"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "RB",
        "label_ko": "우측 풀백",
        "group": "DF",
        "x": 85,
        "y": 73,
        "compatible": [
          "RB",
          "RWB",
          "CB"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LM",
        "label_ko": "좌측 미드필더",
        "group": "MF",
        "x": 16,
        "y": 47,
        "compatible": [
          "LW",
          "LM",
          "CM",
          "CAM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "LCM",
        "label_ko": "좌측 중앙 미드필더",
        "group": "MF",
        "x": 39,
        "y": 50,
        "compatible": [
          "CM",
          "CDM",
          "CAM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "RCM",
        "label_ko": "우측 중앙 미드필더",
        "group": "MF",
        "x": 61,
        "y": 50,
        "compatible": [
          "CM",
          "CDM",
          "CAM"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "RM",
        "label_ko": "우측 미드필더",
        "group": "MF",
        "x": 84,
        "y": 47,
        "compatible": [
          "RW",
          "RM",
          "CM",
          "CAM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "LS",
        "label_ko": "좌측 스트라이커",
        "group": "FW",
        "x": 36,
        "y": 19,
        "compatible": [
          "ST",
          "CF",
          "LW",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "RS",
        "label_ko": "우측 스트라이커",
        "group": "FW",
        "x": 64,
        "y": 19,
        "compatible": [
          "ST",
          "CF",
          "RW",
          "CAM"
        ]
      }
    ]
  },
  {
    "code": "4-1-4-1",
    "name_ko": "4-1-4-1 (원 볼란치 & 2선 압박 블록)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LB",
        "label_ko": "좌측 풀백",
        "group": "DF",
        "x": 15,
        "y": 73,
        "compatible": [
          "LB",
          "LWB",
          "CB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 37,
        "y": 75,
        "compatible": [
          "CB",
          "LCB",
          "RCB"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 63,
        "y": 75,
        "compatible": [
          "CB",
          "RCB",
          "LCB"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "RB",
        "label_ko": "우측 풀백",
        "group": "DF",
        "x": 85,
        "y": 73,
        "compatible": [
          "RB",
          "RWB",
          "CB"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "CDM",
        "label_ko": "수비형 미드필더",
        "group": "MF",
        "x": 50,
        "y": 60,
        "compatible": [
          "CDM",
          "CM",
          "CB"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "LM",
        "label_ko": "좌측 미드필더",
        "group": "MF",
        "x": 16,
        "y": 41,
        "compatible": [
          "LW",
          "LM",
          "CAM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "LCM",
        "label_ko": "좌측 공격형/중앙 MF",
        "group": "MF",
        "x": 38,
        "y": 43,
        "compatible": [
          "CM",
          "CAM",
          "CDM"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "RCM",
        "label_ko": "우측 공격형/중앙 MF",
        "group": "MF",
        "x": 62,
        "y": 43,
        "compatible": [
          "CM",
          "CAM",
          "CDM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "RM",
        "label_ko": "우측 미드필더",
        "group": "MF",
        "x": 84,
        "y": 41,
        "compatible": [
          "RW",
          "RM",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "ST",
        "label_ko": "스트라이커",
        "group": "FW",
        "x": 50,
        "y": 17,
        "compatible": [
          "ST",
          "CF"
        ]
      }
    ]
  },
  {
    "code": "3-5-2",
    "name_ko": "3-5-2 (스리백 & 윙백 지배형 투톱)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LCB",
        "label_ko": "좌측 스토퍼/센터백",
        "group": "DF",
        "x": 26,
        "y": 74,
        "compatible": [
          "CB",
          "LB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "CB",
        "label_ko": "중앙 센터백/리베로",
        "group": "DF",
        "x": 50,
        "y": 76,
        "compatible": [
          "CB",
          "CDM"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 스토퍼/센터백",
        "group": "DF",
        "x": 74,
        "y": 74,
        "compatible": [
          "CB",
          "RB"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "LWB",
        "label_ko": "좌측 윙백",
        "group": "MF",
        "x": 13,
        "y": 50,
        "compatible": [
          "LB",
          "LWB",
          "LW",
          "LM"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LCM",
        "label_ko": "좌측 중앙 미드필더",
        "group": "MF",
        "x": 34,
        "y": 48,
        "compatible": [
          "CM",
          "CAM",
          "CDM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "CDM",
        "label_ko": "수비형 미드필더",
        "group": "MF",
        "x": 50,
        "y": 56,
        "compatible": [
          "CDM",
          "CM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "RCM",
        "label_ko": "우측 중앙 미드필더",
        "group": "MF",
        "x": 66,
        "y": 48,
        "compatible": [
          "CM",
          "CAM",
          "CDM"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "RWB",
        "label_ko": "우측 윙백",
        "group": "MF",
        "x": 87,
        "y": 50,
        "compatible": [
          "RB",
          "RWB",
          "RW",
          "RM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "LS",
        "label_ko": "좌측 스트라이커",
        "group": "FW",
        "x": 36,
        "y": 19,
        "compatible": [
          "ST",
          "CF",
          "LW",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "RS",
        "label_ko": "우측 스트라이커",
        "group": "FW",
        "x": 64,
        "y": 19,
        "compatible": [
          "ST",
          "CF",
          "RW",
          "CAM"
        ]
      }
    ]
  },
  {
    "code": "3-4-3",
    "name_ko": "3-4-3 (토탈 풋볼 & 스리톱 하이프레싱)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 26,
        "y": 74,
        "compatible": [
          "CB",
          "LB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "CB",
        "label_ko": "중앙 센터백",
        "group": "DF",
        "x": 50,
        "y": 76,
        "compatible": [
          "CB",
          "CDM"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 74,
        "y": 74,
        "compatible": [
          "CB",
          "RB"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "LM",
        "label_ko": "좌측 윙백/미드필더",
        "group": "MF",
        "x": 14,
        "y": 50,
        "compatible": [
          "LB",
          "LWB",
          "LM",
          "LW"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LCM",
        "label_ko": "좌측 중앙 미드필더",
        "group": "MF",
        "x": 38,
        "y": 52,
        "compatible": [
          "CM",
          "CDM",
          "CAM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "RCM",
        "label_ko": "우측 중앙 미드필더",
        "group": "MF",
        "x": 62,
        "y": 52,
        "compatible": [
          "CM",
          "CDM",
          "CAM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "RM",
        "label_ko": "우측 윙백/미드필더",
        "group": "MF",
        "x": 86,
        "y": 50,
        "compatible": [
          "RB",
          "RWB",
          "RM",
          "RW"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "LW",
        "label_ko": "좌측 윙포워드",
        "group": "FW",
        "x": 20,
        "y": 23,
        "compatible": [
          "LW",
          "ST",
          "CAM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "ST",
        "label_ko": "스트라이커",
        "group": "FW",
        "x": 50,
        "y": 17,
        "compatible": [
          "ST",
          "CF",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "RW",
        "label_ko": "우측 윙포워드",
        "group": "FW",
        "x": 80,
        "y": 23,
        "compatible": [
          "RW",
          "ST",
          "CAM"
        ]
      }
    ]
  },
  {
    "code": "4-2-2-2",
    "name_ko": "4-2-2-2 (매직 스퀘어 & 듀얼 플레이메이커)",
    "slots": [
      {
        "slot_index": 0,
        "slot_code": "GK",
        "label_ko": "골키퍼",
        "group": "GK",
        "x": 50,
        "y": 88,
        "compatible": [
          "GK"
        ]
      },
      {
        "slot_index": 1,
        "slot_code": "LB",
        "label_ko": "좌측 풀백",
        "group": "DF",
        "x": 15,
        "y": 73,
        "compatible": [
          "LB",
          "LWB",
          "CB"
        ]
      },
      {
        "slot_index": 2,
        "slot_code": "LCB",
        "label_ko": "좌측 센터백",
        "group": "DF",
        "x": 37,
        "y": 75,
        "compatible": [
          "CB",
          "LCB",
          "RCB"
        ]
      },
      {
        "slot_index": 3,
        "slot_code": "RCB",
        "label_ko": "우측 센터백",
        "group": "DF",
        "x": 63,
        "y": 75,
        "compatible": [
          "CB",
          "RCB",
          "LCB"
        ]
      },
      {
        "slot_index": 4,
        "slot_code": "RB",
        "label_ko": "우측 풀백",
        "group": "DF",
        "x": 85,
        "y": 73,
        "compatible": [
          "RB",
          "RWB",
          "CB"
        ]
      },
      {
        "slot_index": 5,
        "slot_code": "LDM",
        "label_ko": "좌측 수비형 미드필더",
        "group": "MF",
        "x": 36,
        "y": 56,
        "compatible": [
          "CDM",
          "CM"
        ]
      },
      {
        "slot_index": 6,
        "slot_code": "RDM",
        "label_ko": "우측 수비형 미드필더",
        "group": "MF",
        "x": 64,
        "y": 56,
        "compatible": [
          "CDM",
          "CM"
        ]
      },
      {
        "slot_index": 7,
        "slot_code": "LAM",
        "label_ko": "좌측 공격형 미드필더",
        "group": "MF",
        "x": 26,
        "y": 36,
        "compatible": [
          "CAM",
          "LW",
          "CM",
          "LM"
        ]
      },
      {
        "slot_index": 8,
        "slot_code": "RAM",
        "label_ko": "우측 공격형 미드필더",
        "group": "MF",
        "x": 74,
        "y": 36,
        "compatible": [
          "CAM",
          "RW",
          "CM",
          "RM"
        ]
      },
      {
        "slot_index": 9,
        "slot_code": "LS",
        "label_ko": "좌측 스트라이커",
        "group": "FW",
        "x": 36,
        "y": 18,
        "compatible": [
          "ST",
          "CF",
          "LW",
          "CAM"
        ]
      },
      {
        "slot_index": 10,
        "slot_code": "RS",
        "label_ko": "우측 스트라이커",
        "group": "FW",
        "x": 64,
        "y": 18,
        "compatible": [
          "ST",
          "CF",
          "RW",
          "CAM"
        ]
      }
    ]
  }
];

  const state = {
    view: 'home', // 'home' | 'builder' | 'database' | 'quality' | 'admin'
    countries: [],
    rankingDate: '2026-10-07',
    formations: DEFAULT_FORMATIONS,
    savedLineups: [],

    // Board state
    boardCountryFilter: 'ALL',
    boardSearch: '',

    // Home filters
    homeSearch: '',
    homeConfed: 'ALL',
    heroPresetIdx: 0,

    // Builder state
    builderCountryCode: 'BRA',
    builderCountryPlayers: [],
    builderFormationCode: '4-3-3',
    builderTeamName: '브라질 역대 최강 XI',
    builderTacticalStyle: '점유율 축구',
    builderBoardTheme: 'classic_emerald',
    builderDescription: '1950년대~2020년대 시대를 초월한 역대 국가대표 베스트11',
    builderSlots: [], // Array of 11 slot objects { slot_index, slot_code, label_ko, group, x, y, compatible, player: null | obj, suitability: {} }
    builderCaptainId: null,
    activeSlotIndex: 9, // Default focused slot (ST)
    swapSourceSlotIndex: null,
    dragSourceSlotIndex: null,
    lastSavedLineupResult: null,

    // Builder candidate filters
    candSearch: '',
    candDecade: 'all',
    candPosFilter: 'slot', // 'slot' | 'all' | 'GK' | 'DF' | 'MF' | 'FW'
    candActiveStatus: 'all',
    candSortBy: 'caps_desc',

    // Arena state
    arenaTeamASlug: 'brazil-all-time-xi',
    arenaTeamBSlug: 'argentina-all-time-xi',
    arenaProvider: 'gemini',
    arenaLoading: false,
    arenaResult: null,
    arenaRecentList: [],

    // Database explorer state
    dbCountryCode: 'BRA',
    dbSearch: '',
    dbDecade: 'all',
    dbPosition: 'all',
    dbActiveStatus: 'all',
    dbSortBy: 'caps_desc',
    dbPlayers: [],
    dbLoading: false,

    // Data quality state
    qualityReport: null,

    // Admin state
    adminLogs: []
  };

  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function formatNameKoEn(p) {
    if (!p) return '';
    const ko = (p.name_ko || '').trim();
    const en = (p.name_en || '').trim();
    if (ko && en && ko.toLowerCase() !== en.toLowerCase()) {
      return `${ko} (${en})`;
    }
    return ko || en;
  }

  function showToast(msg, type = 'info') {
    const root = document.getElementById('toast-root');
    if (!root) return;
    const colors = {
      info: 'bg-slate-900 border-sky-500/60 text-slate-100',
      success: 'bg-emerald-950/95 border-emerald-400 text-emerald-100',
      warn: 'bg-amber-950/95 border-amber-400 text-amber-100',
      error: 'bg-rose-950/95 border-rose-400 text-rose-100'
    };
    const el = document.createElement('div');
    el.className = `pointer-events-auto px-4 py-3 rounded-xl border shadow-2xl text-xs sm:text-sm font-semibold transition-all duration-300 ${colors[type] || colors.info}`;
    el.innerHTML = msg;
    root.appendChild(el);
    setTimeout(() => {
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 300);
    }, 3800);
  }

  function updateNavHighlight() {
    ['home', 'builder', 'board', 'database', 'quality'].forEach(v => {
      const btn = document.getElementById(`nav-${v}`);
      if (!btn) return;
      if (state.view === v) {
        btn.className = 'nav-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-bold whitespace-nowrap bg-amber-400 text-slate-950 shadow-md shadow-amber-400/20';
      } else {
        btn.className = 'nav-btn px-3 py-2 rounded-lg text-xs sm:text-sm font-bold whitespace-nowrap text-slate-300 hover:bg-slate-800/80 hover:text-white';
      }
    });
  }

  function updateAiBadge() {
    const dot = document.getElementById('ai-status-dot');
    const txt = document.getElementById('ai-status-text');
    if (!dot || !txt) return;
    dot.className = 'w-2 h-2 rounded-full bg-emerald-400 animate-pulse';
    txt.textContent = 'AI 전술 시뮬레이터 준비완료';
  }

  // Client-side suitability calculator matching backend rules
  function computeClientSuitability(player, slotDef) {
    if (!player || !slotDef) return { status: '미배치', score: 0, isLow: false };
    const sc = slotDef.slot_code;
    const sgroup = slotDef.group;
    const ppos = player.primary_position;
    let sec = [];
    try {
      sec = typeof player.secondary_positions === 'string' ? JSON.parse(player.secondary_positions || '[]') : (player.secondary_positions || []);
    } catch (e) {
      sec = [];
    }

    const natMap = {
      GK: ['GK'],
      CB: ['CB', 'LCB', 'RCB'],
      LB: ['LB', 'LWB'],
      RB: ['RB', 'RWB'],
      CDM: ['CDM', 'LDM', 'RDM'],
      CM: ['CM', 'LCM', 'RCM'],
      CAM: ['CAM', 'LAM', 'RAM'],
      LW: ['LW', 'LM', 'LAM'],
      RW: ['RW', 'RM', 'RAM'],
      ST: ['ST', 'LS', 'RS', 'CF']
    };
    const adaptMap = {
      GK: [],
      CB: ['CDM', 'LB', 'RB'],
      LB: ['LM', 'LCB', 'LW'],
      RB: ['RM', 'RCB', 'RW'],
      CDM: ['CM', 'LCM', 'RCM', 'CB', 'LCB', 'RCB'],
      CM: ['CDM', 'LDM', 'RDM', 'CAM', 'LM', 'RM'],
      CAM: ['CM', 'LCM', 'RCM', 'LW', 'RW', 'ST', 'LS', 'RS'],
      LW: ['RW', 'RM', 'RAM', 'ST', 'LS', 'CAM', 'LWB'],
      RW: ['LW', 'LM', 'LAM', 'ST', 'RS', 'CAM', 'RWB'],
      ST: ['LW', 'RW', 'LAM', 'RAM', 'CAM']
    };

    if ((natMap[ppos] || [ppos]).includes(sc)) {
      return { status: '적합', score: 100, isLow: false };
    }
    for (const sp of sec) {
      if ((natMap[sp] || [sp]).includes(sc)) {
        return { status: '부포지션 적합', score: 90, isLow: false };
      }
    }
    if ((adaptMap[ppos] || []).includes(sc) || (slotDef.compatible || []).includes(ppos)) {
      return { status: '부포지션 호환', score: 78, isLow: false };
    }
    if (player.position_group === sgroup && ppos !== 'GK' && sc !== 'GK') {
      return { status: '부포지션 호환', score: 72, isLow: false };
    }
    return { status: '포지션 적합도 낮음', score: 35, isLow: true };
  }

  // Render an avatar / portrait with graceful fallback on error or missing URL (Test H)
  function renderPlayerAvatarHtml(player, countryObj, sizeClass = 'w-11 h-11', textClass = 'text-xs') {
    const kp = (countryObj && countryObj.kit_primary_color) || '#facc15';
    const ks = (countryObj && countryObj.kit_secondary_color) || '#15803d';
    const kt = (countryObj && countryObj.kit_text_color) || '#0f172a';
    const num = (player && (player.jersey_number || player.fallback_number)) || (player && player.primary_position === 'GK' ? 1 : 10);
    const initials = (player && player.fallback_initials) || (player && player.name_en ? player.name_en.slice(0, 2).toUpperCase() : 'XI');
    const imgUrl = player && player.image_url;

    const fallbackBadge = `<div class="${sizeClass} rounded-full flex flex-col items-center justify-center font-black leading-none select-none shadow-inner" style="background:${kp}; color:${kt}; border:2px solid ${ks};">
      <span class="${textClass}">${escapeHtml(num)}</span>
    </div>`;

    if (!imgUrl) {
      return fallbackBadge;
    }

    return `<div class="relative ${sizeClass} rounded-full overflow-hidden flex items-center justify-center shrink-0" style="background:${kp}; color:${kt}; border:2px solid ${ks};">
      <span class="font-black ${textClass} select-none">${escapeHtml(num)}</span>
      <img src="${escapeHtml(imgUrl)}" alt="${escapeHtml(player.name_ko)}" loading="lazy"
           class="absolute inset-0 w-full h-full object-cover object-top"
           onerror="this.style.display='none'" />
    </div>`;
  }

  // Render Interactive SVG Football Pitch HTML
  function renderTacticalPitchHtml(options) {
    const {
      slots = [],
      country = {},
      themeId = 'classic_emerald',
      interactive = false,
      compact = false
    } = options;

    const theme = BOARD_THEMES.find(t => t.id === themeId) || BOARD_THEMES[0];
    const kp = country.kit_primary_color || '#facc15';
    const ks = country.kit_secondary_color || '#15803d';
    const kt = country.kit_text_color || '#0f172a';

    // 12 horizontal grass stripes inside SVG
    let stripesSvg = '';
    for (let i = 0; i < 12; i++) {
      const y = (i * 100) / 12;
      const h = 100 / 12 + 0.2;
      const fill = i % 2 === 0 ? theme.light : theme.dark;
      stripesSvg += `<rect x="0" y="${y}" width="100" height="${h}" fill="${fill}" />`;
    }

    const nodesHtml = slots.map((slot, idx) => {
      const p = slot.player;
      const isFocused = interactive && state.activeSlotIndex === idx;
      const isSwapSelected = interactive && state.swapSourceSlotIndex === idx;
      const isCap = p && (slot.is_captain || (state.builderCaptainId && state.builderCaptainId === p.id) || p.is_captain);
      const suit = p ? (slot.suitability || { status: p.suitability_status || '적합', isLow: (p.suitability_status || '').includes('낮음') }) : null;
      const lowSuit = suit && suit.isLow;

      const ringColor = isSwapSelected
        ? '#38bdf8'
        : isCap
        ? '#facc15'
        : lowSuit
        ? '#f87171'
        : isFocused
        ? '#34d399'
        : ks;

      // Perfectly proportioned node sizing to prevent any overlap
      const nodeSize = compact ? 'w-9 h-9 sm:w-10 sm:h-10' : 'w-11 h-11 sm:w-13 sm:h-13';
      const nameMaxW = compact ? 'max-w-[70px]' : 'max-w-[84px] sm:max-w-[104px]';

      if (!p) {
        return `
          <div class="pitch-node absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer group"
               style="left:${slot.x}%; top:${slot.y}%;"
               ${interactive ? `onclick="window.app.onPitchSlotClick(${idx})" ondragover="event.preventDefault()" ondrop="window.app.onPitchSlotDrop(event, ${idx})"` : ''}>
            <div class="${nodeSize} rounded-full border-2 border-dashed ${isFocused ? 'border-amber-400 bg-amber-400/20 scale-105' : 'border-white/50 bg-slate-950/60 group-hover:border-amber-300'} flex flex-col items-center justify-center transition shadow-md">
              <span class="text-[9px] sm:text-[10px] font-black text-amber-300 leading-none">${escapeHtml(slot.slot_code)}</span>
              <span class="text-[8px] text-slate-300 leading-none mt-0.5">+선택</span>
            </div>
            <div class="mt-0.5 px-1.5 py-0.5 rounded bg-slate-950/90 border border-slate-700 text-[9px] text-slate-300 font-semibold whitespace-nowrap shadow">
              ${escapeHtml(slot.label_ko || slot.slot_code)}
            </div>
          </div>
        `;
      }

      const num = p.jersey_number || p.fallback_number || (idx + 1);
      const displayName = p.name_ko || p.name_en || '선수';
      const fullName = formatNameKoEn(p);

      return `
        <div class="pitch-node ${isSwapSelected ? 'selected-swap' : ''} absolute -translate-x-1/2 -translate-y-1/2 flex flex-col items-center cursor-pointer"
             style="left:${slot.x}%; top:${slot.y}%;"
             ${interactive ? `draggable="true" ondragstart="window.app.onPitchSlotDragStart(event, ${idx})" ondragover="event.preventDefault()" ondrop="window.app.onPitchSlotDrop(event, ${idx})" onclick="window.app.onPitchSlotClick(${idx})"` : `onclick="window.app.openPlayerModal(${p.player_id || p.id})"`}>
          <div class="relative">
            <!-- Slot code pill -->
            <span class="absolute -top-1.5 -left-2 z-20 px-1 py-0.2 rounded bg-slate-950 text-[8px] sm:text-[9px] font-black text-white border shadow" style="border-color:${ringColor}">
              ${escapeHtml(slot.slot_code)}
            </span>
            ${isCap ? `<span class="absolute -top-1.5 -right-2 z-20 w-4 h-4 rounded-full bg-amber-400 text-slate-950 text-[9px] font-black flex items-center justify-center border border-slate-950 shadow" title="주장 (Captain)">C</span>` : ''}
            <!-- Portrait or Jersey Circle -->
            <div class="relative ${nodeSize} rounded-full overflow-hidden flex items-center justify-center shadow-lg"
                 style="background:${kp}; color:${kt}; border:2.5px solid ${ringColor};">
              <span class="font-black text-xs sm:text-base select-none">${escapeHtml(num)}</span>
              ${p.image_url ? `<img src="${escapeHtml(p.image_url)}" alt="${escapeHtml(p.name_ko)}" class="absolute inset-0 w-full h-full object-cover object-top" onerror="this.style.display='none'" />` : ''}
            </div>
          </div>
          <!-- Player Name & Caps Plate: Safe line-height & padding prevents text clipping -->
          <div class="mt-0.5 px-1.5 py-0.5 rounded-md bg-slate-950/95 border ${lowSuit ? 'border-rose-500' : isFocused ? 'border-amber-400' : 'border-slate-700/80'} text-center shadow-md text-[10px] sm:text-xs" style="line-height: 1.35;">
            <div class="font-black text-white truncate ${nameMaxW}" style="line-height: 1.35; padding: 1px 0;" title="${escapeHtml(fullName)}">${escapeHtml(displayName)}</div>
            ${!compact ? `<div class="text-[9px] text-amber-300 font-bold leading-tight whitespace-nowrap" style="padding-bottom: 1px;">${escapeHtml(p.official_caps)}경기</div>` : ''}
            ${lowSuit ? `<div class="text-[8px] font-bold text-rose-400 leading-tight">⚠ 적합도 낮음</div>` : ''}
          </div>
        </div>
      `;
    }).join('');

    return `
      <div id="tactical-pitch-board" class="relative w-full aspect-[4/5] max-w-[660px] mx-auto rounded-2xl overflow-hidden border-2 border-slate-700/80 shadow-2xl select-none">
        <svg viewBox="0 0 100 100" preserveAspectRatio="none" class="absolute inset-0 w-full h-full">
          ${stripesSvg}
          <!-- Pitch markings -->
          <g fill="none" stroke="${theme.border}" stroke-width="0.45">
            <!-- Outer boundary -->
            <rect x="4.5" y="4" width="91" height="92" />
            <!-- Halfway line & Center circle -->
            <line x1="4.5" y1="50" x2="95.5" y2="50" />
            <circle cx="50" cy="50" r="11.5" />
            <circle cx="50" cy="50" r="0.7" fill="${theme.border}" />
            <!-- Top Penalty Box (Attack Direction) -->
            <rect x="22" y="4" width="56" height="15" />
            <rect x="36" y="4" width="28" height="5.5" />
            <rect x="43" y="1.8" width="14" height="2.2" />
            <path d="M 41 19 A 9 9 0 0 0 59 19" />
            <!-- Bottom Penalty Box (GK Direction) -->
            <rect x="22" y="81" width="56" height="15" />
            <rect x="36" y="90.5" width="28" height="5.5" />
            <rect x="43" y="96" width="14" height="2.2" />
            <path d="M 41 81 A 9 9 0 0 1 59 81" />
            <!-- Corner arcs -->
            <path d="M 4.5 6 A 2 2 0 0 0 6.5 4" />
            <path d="M 93.5 4 A 2 2 0 0 0 95.5 6" />
            <path d="M 4.5 94 A 2 2 0 0 1 6.5 96" />
            <path d="M 93.5 96 A 2 2 0 0 1 95.5 94" />
          </g>
        </svg>
        <!-- Direction watermark -->
        <div class="absolute top-1.5 left-1/2 -translate-x-1/2 text-[9px] font-bold tracking-widest uppercase text-white/40 pointer-events-none">
          ▲ ATTACK (공격 방향)
        </div>
        <!-- 11 Player Slot Nodes -->
        <div class="absolute inset-0">
          ${nodesHtml}
        </div>
      </div>
    `;
  }

  // ============================================================================
  // VIEW 1: HOME & COUNTRY SELECTION
  // ============================================================================
  function renderHomeView() {
    const heroLineup = state.savedLineups[state.heroPresetIdx] ? state.savedLineups[state.heroPresetIdx].snapshot : null;
    let heroPitchHtml = '';
    if (heroLineup) {
      const heroSlots = (heroLineup.players || []).map(p => ({
        slot_index: p.slot_index,
        slot_code: p.slot_code,
        label_ko: p.slot_label_ko || p.slot_code,
        x: p.x,
        y: p.y,
        player: p,
        is_captain: p.is_captain,
        suitability: { status: p.suitability_status || '적합', isLow: (p.suitability_status || '').includes('낮음') }
      }));
      heroPitchHtml = renderTacticalPitchHtml({
        slots: heroSlots,
        country: heroLineup,
        themeId: heroLineup.board_color_theme || 'classic_emerald',
        interactive: false,
        compact: true
      });
    }

    const filteredCountries = state.countries.filter(c => {
      if (state.homeConfed !== 'ALL' && c.confederation !== state.homeConfed) return false;
      if (state.homeSearch.trim()) {
        const q = state.homeSearch.trim().toLowerCase();
        return (
          (c.name_ko || '').toLowerCase().includes(q) ||
          (c.name_en || '').toLowerCase().includes(q) ||
          (c.fifa_code || '').toLowerCase().includes(q)
        );
      }
      return true;
    });

    const confeds = ['ALL', 'UEFA', 'CONMEBOL', 'CONCACAF', 'CAF', 'AFC'];

    return `
      <!-- Hero Banner with Live Tactical Pitch -->
      <section class="relative rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900/95 to-emerald-950/60 border border-slate-800 p-5 sm:p-8 lg:p-10 mb-8 overflow-hidden shadow-2xl">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-7 space-y-5">
            <div class="inline-flex flex-wrap items-center gap-2 px-3 py-1 rounded-full bg-amber-400/10 border border-amber-400/30 text-amber-300 text-xs font-bold">
              <span>🏆 FIFA 세계랭킹 TOP 30 (기준일: ${escapeHtml(state.rankingDate)})</span>
              <span>·</span>
              <span>성인 남자 A매치 30회 이상 공식 기록 검증</span>
            </div>
            <h1 class="text-[clamp(1.75rem,3.4vw,3.2rem)] font-black tracking-tight text-white leading-[1.25]">
              <span class="block">역대 최강의 국가대표,</span>
              <span class="block mt-1"><span class="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 via-yellow-400 to-emerald-400">베스트 일레븐</span>을 완성하라</span>
            </h1>
            <p class="text-slate-300 text-sm sm:text-base leading-relaxed max-w-2xl">
              1950·60년대 펠레·가린샤·보비 찰턴부터 1970·80년대 마라도나·베켄바워·크라위프·지쿠, 1990·2000년대 호나우두·지단·말디니, 2010·2020년대 메시·호날두·네이마르·음바페까지.<br/>
              <strong>실제 A매치 30회 이상 출전 기록이 검증된 3,817명</strong>의 데이터베이스로 나만의 전술판을 제작하고, 고해상도 PNG 이미지 및 공유 링크로 간직하세요.
            </p>

            <!-- Primary Action Buttons -->
            <div class="flex flex-wrap gap-3 pt-2">
              <button onclick="window.app.startCountryBuilder('BRA')" class="px-5 py-3.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm sm:text-base shadow-lg shadow-amber-400/20 transition flex items-center gap-2">
                <span>⚽ 나만의 역대 베스트11 만들기</span>
              </button>
              <button onclick="window.app.navigate('database')" class="px-5 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white border border-slate-700 font-bold text-sm sm:text-base transition flex items-center gap-2">
                <span>🔍 역대 국가대표 선수 검색</span>
              </button>
            </div>

            <!-- Key stats bar -->
            <div class="grid grid-cols-3 gap-3 pt-3 max-w-lg">
              <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                <div class="text-xl sm:text-2xl font-black text-amber-400">30개국</div>
                <div class="text-[11px] text-slate-400">FIFA 랭킹 1~30위</div>
              </div>
              <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                <div class="text-xl sm:text-2xl font-black text-emerald-400">3,817명</div>
                <div class="text-[11px] text-slate-400">A매치 30회+ 검증 선수</div>
              </div>
              <div class="p-3 rounded-xl bg-slate-950/70 border border-slate-800">
                <div class="text-xl sm:text-2xl font-black text-sky-400">1900s–2020s</div>
                <div class="text-[11px] text-slate-400">전 시대 대표팀 망라</div>
              </div>
            </div>
          </div>

          <!-- Right Hero Live Tactical Board Showcase -->
          <div class="lg:col-span-5 bg-slate-950/80 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex items-center justify-between gap-2 mb-3">
              <div>
                <span class="text-[11px] font-bold uppercase tracking-wider text-amber-400">FEATURED DREAM XI</span>
                <h3 class="text-sm sm:text-base font-black text-white truncate">
                  ${heroLineup ? `${escapeHtml(heroLineup.flag_emoji || '')} ${escapeHtml(heroLineup.team_name)} (${escapeHtml(heroLineup.formation_code)})` : '대표 드림팀 예시'}
                </h3>
              </div>
              <div class="flex items-center gap-1.5">
                ${state.savedLineups.slice(0, 3).map((item, idx) => `
                  <button onclick="window.app.setHeroPreset(${idx})"
                          class="px-2.5 py-1 rounded-lg text-xs font-bold border transition ${state.heroPresetIdx === idx ? 'bg-amber-400 text-slate-950 border-amber-400' : 'bg-slate-900 text-slate-300 border-slate-700 hover:bg-slate-800'}">
                    ${escapeHtml(item.country_name_ko)}
                  </button>
                `).join('')}
              </div>
            </div>
            ${heroPitchHtml}
            ${heroLineup ? `
              <div class="mt-3 flex flex-wrap items-center justify-between gap-2 text-xs">
                <span class="text-slate-400 truncate max-w-[240px]">💡 선수를 클릭하면 상세 기록을 볼 수 있습니다</span>
                <div class="flex items-center gap-2">
                  <button onclick="window.app.loadSavedLineupIntoBuilder('${escapeHtml(heroLineup.share_slug)}')" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold border border-slate-700">
                    전술판에서 열기 →
                  </button>
                </div>
              </div>
            ` : ''}
          </div>
        </div>
      </section>

      <!-- Country Selection Section (Section 2 & 4-1) -->
      <section class="space-y-4">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 bg-slate-900/80 border border-slate-800 rounded-2xl p-4 sm:p-5">
          <div>
            <div class="flex items-center gap-2">
              <h2 class="text-xl sm:text-2xl font-black text-white">국가 선택 (FIFA 세계랭킹 1~30위)</h2>
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-sky-500/15 text-sky-300 border border-sky-500/30">
                랭킹 기준일: ${escapeHtml(state.rankingDate)}
              </span>
            </div>
            <p class="text-xs sm:text-sm text-slate-400 mt-1">
              원하는 국가를 클릭하면 해당 국가의 역대 A매치 30회 이상 선수들로 베스트11 전술판을 제작할 수 있습니다. (현재 FIFA 랭킹은 대상 30개국 선정 기준이며 역대 팀 전력 평가에 영향을 주지 않습니다.)
            </p>
          </div>

          <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2.5">
            <input type="text"
                   value="${escapeHtml(state.homeSearch)}"
                   oninput="window.app.onHomeSearch(this.value)"
                   placeholder="국가명 검색 (예: 브라질, Brazil, KOR...)"
                   class="px-3.5 py-2 rounded-xl bg-slate-950 border border-slate-700 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-amber-400 w-full sm:w-64" />
            <div class="flex items-center gap-1 overflow-x-auto pb-1 sm:pb-0">
              ${confeds.map(cf => `
                <button onclick="window.app.onHomeConfed('${cf}')"
                        class="px-2.5 py-1.5 rounded-lg text-xs font-bold whitespace-nowrap transition ${state.homeConfed === cf ? 'bg-amber-400 text-slate-950' : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'}">
                  ${cf === 'ALL' ? '전체(30)' : cf}
                </button>
              `).join('')}
            </div>
          </div>
        </div>

        <!-- 30 Countries Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-3.5">
          ${filteredCountries.map(c => `
            <div onclick="window.app.startCountryBuilder('${escapeHtml(c.fifa_code)}')"
                 class="group relative rounded-2xl bg-slate-900/90 hover:bg-slate-800/95 border border-slate-800 hover:border-amber-400/70 p-4 cursor-pointer transition-all duration-200 flex flex-col justify-between shadow-lg hover:shadow-amber-400/5">
              <div>
                <div class="flex items-center justify-between gap-2 mb-3">
                  <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded-md bg-slate-950 border border-slate-700 text-xs font-black text-amber-400">
                      #${c.fifa_rank}
                    </span>
                    <span class="text-[11px] font-bold text-slate-400">${escapeHtml(c.confederation)} · ${escapeHtml(c.fifa_code)}</span>
                  </div>
                  <span class="text-[11px] font-semibold text-slate-400">${Number(c.fifa_points).toFixed(2)} pts</span>
                </div>

                <div class="flex items-center gap-3 mb-3">
                  <div class="w-12 h-9 rounded-lg overflow-hidden bg-slate-950 border border-slate-700 flex items-center justify-center shrink-0 shadow">
                    ${c.flag_svg_url
                      ? `<img src="${escapeHtml(c.flag_svg_url)}" alt="${escapeHtml(c.name_ko)}" class="w-full h-full object-cover" onerror="this.outerHTML='<span class=\\'text-2xl\\'>${escapeHtml(c.flag_emoji)}</span>'" />`
                      : `<span class="text-2xl">${escapeHtml(c.flag_emoji)}</span>`}
                  </div>
                  <div class="min-w-0">
                    <div class="font-black text-base text-white group-hover:text-amber-300 transition truncate">${escapeHtml(c.name_ko)}</div>
                    <div class="text-xs text-slate-400 truncate">${escapeHtml(c.name_en)}</div>
                  </div>
                </div>

                <!-- World Cup & Major Honors -->
                <div class="space-y-1.5 mb-3">
                  ${c.world_cup_titles > 0
                    ? `<div class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-amber-400/15 border border-amber-400/40 text-amber-300 text-[11px] font-bold">
                        🏆 월드컵 우승 ${c.world_cup_titles}회 (${escapeHtml(c.world_cup_winning_years)})
                       </div>`
                    : `<div class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md bg-slate-950 border border-slate-800 text-slate-400 text-[11px]">
                        국제대회 주요 성과 보유
                       </div>`}
                  <p class="text-[11px] text-slate-300 line-clamp-2 leading-snug">${escapeHtml(c.major_honors_ko || '')}</p>
                </div>
              </div>

              <div class="pt-3 border-t border-slate-800/80 flex items-center justify-between">
                <div class="flex items-center gap-1.5">
                  <span class="w-2.5 h-2.5 rounded-full border border-white/40" style="background:${escapeHtml(c.kit_primary_color)}"></span>
                  <span class="text-xs font-bold text-emerald-400">선정 가능 ${c.eligible_player_count}명</span>
                </div>
                <span class="text-xs font-bold text-slate-400 group-hover:text-amber-400 transition">베스트11 만들기 →</span>
              </div>
            </div>
          `).join('')}
        </div>
      </section>
    `;
  }

  // ============================================================================
  // VIEW 2: BEST 11 TACTICAL BOARD BUILDER
  // ============================================================================
  function getBuilderCountryObj() {
    return state.countries.find(c => c.fifa_code === state.builderCountryCode) || state.countries[0] || {};
  }

  function renderBuilderView() {
    const country = getBuilderCountryObj();
    const filledCount = state.builderSlots.filter(s => s.player).length;
    const focusedSlot = state.builderSlots[state.activeSlotIndex] || state.builderSlots[0];
    const usedPlayerIds = new Set(state.builderSlots.filter(s => s.player).map(s => s.player.id || s.player.player_id));

    // Filter candidates for the right-hand selection drawer
    // When user types a direct search query, search across ALL positions of the country so any player can be found immediately
    const isDirectSearching = Boolean(state.candSearch.trim());
    const candidates = state.builderCountryPlayers.filter(p => {
      if (isDirectSearching) {
        const q = state.candSearch.trim().toLowerCase();
        const match =
          formatNameKoEn(p).toLowerCase().includes(q) ||
          (p.name_ko || '').toLowerCase().includes(q) ||
          (p.name_en || '').toLowerCase().includes(q) ||
          (p.aliases_search || '').toLowerCase().includes(q) ||
          (p.major_clubs_ko || '').toLowerCase().includes(q);
        if (!match) return false;
      }
      if (state.candDecade !== 'all') {
        if (state.candDecade === 'pre1960') {
          const y1 = p.career_start_year || 2000;
          if (y1 >= 1960) return false;
        } else {
          const dtags = p.decade_tags || '';
          if (!dtags.includes(state.candDecade) && p.primary_decade !== state.candDecade) return false;
        }
      }
      if (state.candActiveStatus === 'active' && !p.is_active_player) return false;
      if (state.candActiveStatus === 'retired' && p.is_active_player) return false;

      if (!isDirectSearching && state.candPosFilter === 'slot' && focusedSlot) {
        if (focusedSlot.slot_code === 'GK') return p.primary_position === 'GK';
        if (p.primary_position === 'GK') return false;
        const suit = computeClientSuitability(p, focusedSlot);
        return !suit.isLow;
      } else if (['GK', 'DF', 'MF', 'FW'].includes(state.candPosFilter)) {
        return p.position_group === state.candPosFilter;
      }
      return true;
    });

    // Sort candidates: default is A-match official_caps DESC (출전 경기 순)
    candidates.sort((a, b) => {
      if (state.candSortBy === 'goals_desc') return (b.official_goals - a.official_goals) || (b.official_caps - a.official_caps);
      if (state.candSortBy === 'name_asc') return (a.name_ko || '').localeCompare(b.name_ko || '', 'ko');
      if (state.candSortBy === 'debut_asc') return (a.career_start_year || 9999) - (b.career_start_year || 9999);
      if (state.candSortBy === 'debut_desc') return (b.career_start_year || 0) - (a.career_start_year || 0);
      return (b.official_caps - a.official_caps) || (b.official_goals - a.official_goals);
    });

    const pitchHtml = renderTacticalPitchHtml({
      slots: state.builderSlots,
      country,
      themeId: state.builderBoardTheme,
      interactive: true,
      compact: false
    });

    return `
      <!-- Top Builder Control Bar -->
      <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-4 mb-5 shadow-xl">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-3">
            <!-- Country selector dropdown -->
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-400">국가:</span>
              <select onchange="window.app.startCountryBuilder(this.value)"
                      class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-sm font-black text-white focus:border-amber-400">
                ${state.countries.map(c => `
                  <option value="${escapeHtml(c.fifa_code)}" ${c.fifa_code === state.builderCountryCode ? 'selected' : ''}>
                    #${c.fifa_rank} ${escapeHtml(c.flag_emoji)} ${escapeHtml(c.name_ko)} (${c.eligible_player_count}명)
                  </option>
                `).join('')}
              </select>
            </div>

            <!-- Formation selector (7 formations) -->
            <div class="flex items-center gap-1.5 flex-wrap">
              <span class="text-xs font-bold text-slate-400">포메이션:</span>
              ${state.formations.map(fm => `
                <button onclick="window.app.changeBuilderFormation('${escapeHtml(fm.code)}')"
                        class="px-2.5 py-1.5 rounded-lg text-xs font-black transition ${state.builderFormationCode === fm.code ? 'bg-amber-400 text-slate-950 shadow' : 'bg-slate-950 text-slate-300 border border-slate-800 hover:border-slate-600'}">
                  ${escapeHtml(fm.code)}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Action Buttons: Smart Auto-Fill, Clear, Save & PNG Export -->
          <div class="flex flex-wrap items-center gap-2">
            <button onclick="window.app.autoFillBuilderLegendXI()"
                    class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-amber-300 border border-slate-700 text-xs font-bold transition">
              ⚡ 레전드 11명 자동 배치
            </button>
            <button onclick="window.app.clearBuilderSlots()"
                    class="px-3 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-400 border border-slate-800 text-xs font-bold transition">
              초기화
            </button>
            <button onclick="window.app.shareLineupDirectly()"
                    class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-xs sm:text-sm font-bold transition flex items-center gap-1.5"
                    title="전술판 접속 링크를 카카오톡 또는 SNS로 공유합니다">
              <span>🔗 링크 공유</span>
            </button>
            <button onclick="window.app.saveCurrentLineup(false)"
                    class="px-3.5 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs sm:text-sm font-black shadow-lg shadow-emerald-500/20 transition">
              💾 팀 저장 (${filledCount}/11)
            </button>
            <button onclick="window.app.exportCurrentLineupPng('portrait', 1)"
                    class="px-3.5 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs sm:text-sm font-black shadow-lg shadow-amber-400/20 transition">
              🖼️ PNG 이미지 저장
            </button>
          </div>
        </div>

        ${country.historical_note_ko ? `
          <div class="mt-3 pt-2.5 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-2 text-xs text-slate-400">
            <div>📌 <strong>역사적 기록 기준:</strong> ${escapeHtml(country.historical_note_ko)}</div>
            <div class="text-amber-300/90 font-semibold">💡 팁: 전술판의 포지션을 클릭하면 A매치 최다 출전 순 추천 선수가 나타나며, 직접 검색해서 배치할 수도 있습니다.</div>
          </div>
        ` : ''}
      </div>

      <!-- Saved Share URL & Export Banner (appears when saved or loaded) -->
      ${state.lastSavedLineupResult ? `
        <div class="rounded-2xl bg-emerald-950/60 border border-emerald-500/50 p-4 mb-5 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4 shadow-xl">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <span class="px-2 py-0.5 rounded bg-emerald-400 text-slate-950 text-xs font-black">완성 완료</span>
              <span class="font-black text-white text-base">${escapeHtml(state.lastSavedLineupResult.lineup.team_name)}</span>
            </div>
            <div class="text-xs text-emerald-200 flex flex-wrap items-center gap-2">
              <span>고유 공유 URL:</span>
              <code class="px-2 py-0.5 rounded bg-slate-950 text-amber-300 font-mono">${escapeHtml(window.location.origin + state.lastSavedLineupResult.share_url)}</code>
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-2">
            <button onclick="window.app.copyShareUrl('${escapeHtml(window.location.origin + state.lastSavedLineupResult.share_url)}')"
                    class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white border border-slate-700 text-xs font-bold">
              🔗 URL 복사
            </button>
            <a href="${escapeHtml(state.lastSavedLineupResult.png_portrait_url)}" download
               class="px-3 py-1.5 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs font-black">
              ⬇️ 세로형 PNG (1080×1350)
            </a>
            <a href="${escapeHtml(state.lastSavedLineupResult.png_landscape_url)}" download
               class="px-3 py-1.5 rounded-lg bg-sky-400 hover:bg-sky-300 text-slate-950 text-xs font-black">
              ⬇️ 가로형 PNG (1200×675)
            </a>
            <a href="${escapeHtml(state.lastSavedLineupResult.png_portrait_url)}&scale=2" download
               class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 border border-amber-400/40 text-xs font-bold">
              ✨ 2x 초고해상도 PNG
            </a>
          </div>
        </div>
      ` : ''}

      <!-- Main 3-Column Builder Layout: Pitch (Left/Center) | Squad & Team Settings (Middle) | Candidate Selector (Right) -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        <!-- Column 1: Interactive Tactical Pitch (5 cols on lg) -->
        <div class="lg:col-span-5 space-y-3">
          <div class="flex items-center justify-between px-1">
            <div class="flex items-center gap-2">
              <span class="text-xl">${escapeHtml(country.flag_emoji || '')}</span>
              <span class="font-black text-white text-base">${escapeHtml(state.builderTeamName)}</span>
              <span class="text-xs px-2 py-0.5 rounded bg-slate-800 text-amber-400 font-bold">${escapeHtml(state.builderFormationCode)}</span>
            </div>
            <div class="flex items-center gap-1.5">
              ${ state.swapSourceSlotIndex !== null ? `
                <button onclick="window.app.cancelSwapMode()" class="px-2.5 py-1 rounded bg-sky-500 text-slate-950 text-xs font-black animate-pulse">
                  교체할 대상 슬롯을 클릭하세요 (취소 ✕)
                </button>
              ` : `
                <span class="text-xs text-slate-400">배치: <strong class="text-amber-400">${filledCount}/11명</strong></span>
              `}
            </div>
          </div>

          ${pitchHtml}

          <!-- Quick PNG Export Bar under Pitch -->
          <div class="rounded-xl bg-slate-900/90 border border-slate-800 p-3 flex flex-wrap items-center justify-between gap-2">
            <span class="text-xs font-bold text-slate-300">즉시 이미지 저장:</span>
            <div class="flex flex-wrap items-center gap-1.5">
              <button onclick="window.app.exportCurrentLineupPng('portrait', 1)" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-bold border border-slate-700">
                📱 세로형 PNG (1080×1350)
              </button>
              <button onclick="window.app.exportCurrentLineupPng('landscape', 1)" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-sky-300 text-xs font-bold border border-slate-700">
                🖥️ 가로형 PNG (1200×675)
              </button>
              <button onclick="window.app.exportCurrentLineupPng('portrait', 2)" class="px-2.5 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-emerald-300 text-xs font-bold border border-slate-700">
                ✨ 고해상도 2x PNG
              </button>
            </div>
          </div>
        </div>

        <!-- Column 2: Selected 11 Squad List & Team Customization (3 cols on lg) -->
        <div class="lg:col-span-3 space-y-4">
          <!-- Team Metadata Settings (Section 4-5) -->
          <div class="rounded-2xl bg-slate-900/90 border border-slate-800 p-4 space-y-3">
            <h3 class="text-sm font-black text-amber-400 uppercase tracking-wider">팀 설정 (TEAM SETTINGS)</h3>
            <div>
              <label class="block text-[11px] font-bold text-slate-400 mb-1">팀 이름</label>
              <input type="text" value="${escapeHtml(state.builderTeamName)}"
                     oninput="window.app.onBuilderMetaChange('teamName', this.value)"
                     placeholder="예: 브라질 역대 최강 XI"
                     class="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white font-bold focus:border-amber-400 focus:outline-none" />
            </div>
            <div class="grid grid-cols-2 gap-2">
              <div>
                <label class="block text-[11px] font-bold text-slate-400 mb-1">전술 스타일</label>
                <select onchange="window.app.onBuilderMetaChange('tacticalStyle', this.value)"
                        class="w-full px-2.5 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white font-semibold">
                  ${TACTICAL_STYLES.map(ts => `<option value="${ts}" ${state.builderTacticalStyle === ts ? 'selected' : ''}>${ts}</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block text-[11px] font-bold text-slate-400 mb-1">전술판 색상</label>
                <select onchange="window.app.onBuilderMetaChange('boardTheme', this.value)"
                        class="w-full px-2.5 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-white font-semibold">
                  ${BOARD_THEMES.map(bt => `<option value="${bt.id}" ${state.builderBoardTheme === bt.id ? 'selected' : ''}>${bt.name}</option>`).join('')}
                </select>
              </div>
            </div>
            <div>
              <label class="block text-[11px] font-bold text-slate-400 mb-1">팀 설명 (선택)</label>
              <input type="text" value="${escapeHtml(state.builderDescription)}"
                     oninput="window.app.onBuilderMetaChange('description', this.value)"
                     placeholder="팀 컨셉 및 전술 설명..."
                     class="w-full px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-xs text-slate-200 focus:border-amber-400 focus:outline-none" />
            </div>

            <!-- Prominent Save Buttons inside Team Settings -->
            <div class="pt-2 space-y-2 border-t border-slate-800">
              <button onclick="window.app.saveCurrentLineup(false)"
                      class="w-full py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs sm:text-sm shadow-lg shadow-emerald-500/20 transition flex items-center justify-center gap-2">
                <span>💾 베스트11 팀 정보 저장하기 (${filledCount}/11명)</span>
              </button>
              <div class="flex gap-1.5">
                <button onclick="window.app.saveDraftToStorage()"
                        class="w-1/2 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold border border-slate-700">
                  📁 임시 보관 (브라우저)
                </button>
                <button onclick="window.app.navigate('board')"
                        class="w-1/2 py-1.5 rounded-lg bg-slate-950 hover:bg-slate-800 text-amber-300 text-xs font-bold border border-slate-800 flex items-center justify-center gap-1">
                  <span>📋</span>
                  <span>베스트11 갤러리</span>
                </button>
              </div>
            </div>
          </div>

          <!-- Current 11 Slots List (Section 5: 전술판 옆에는 현재 선택된 선수 11명의 목록을 표시한다) -->
          <div class="rounded-2xl bg-slate-900/90 border border-slate-800 p-3.5 space-y-2">
            <div class="flex items-center justify-between">
              <h3 class="text-sm font-black text-white">현재 선택된 베스트11 (${filledCount}/11)</h3>
              <span class="text-[11px] text-slate-400">클릭 시 포지션 추천·교체</span>
            </div>
            <div class="space-y-1.5 max-h-[520px] overflow-y-auto custom-scrollbar pr-1">
              ${state.builderSlots.map((slot, idx) => {
                const p = slot.player;
                const isFocused = state.activeSlotIndex === idx;
                const isCap = p && (slot.is_captain || (state.builderCaptainId && state.builderCaptainId === p.id));
                const suit = p ? (slot.suitability || { status: '적합', isLow: false }) : null;
                return `
                  <div onclick="window.app.onPitchSlotClick(${idx})"
                       class="p-2 rounded-xl border transition cursor-pointer flex items-center justify-between gap-2 ${isFocused ? 'bg-amber-400/15 border-amber-400' : 'bg-slate-950/80 border-slate-800 hover:border-slate-700'}">
                    <div class="flex items-center gap-2 min-w-0">
                      <span class="w-9 text-center py-1 rounded bg-slate-900 border border-slate-700 text-[11px] font-black text-amber-400 shrink-0">
                        ${escapeHtml(slot.slot_code)}
                      </span>
                      ${p ? `
                        <div class="min-w-0">
                          <div class="flex items-center gap-1">
                            <span class="text-xs font-bold text-white truncate" title="${escapeHtml(formatNameKoEn(p))}">${escapeHtml(formatNameKoEn(p))}</span>
                            <span class="text-[10px] text-slate-400 shrink-0">[${escapeHtml(p.primary_position)}]</span>
                            ${isCap ? `<span class="px-1 rounded bg-amber-400 text-slate-950 text-[9px] font-black shrink-0">C</span>` : ''}
                          </div>
                          <div class="flex items-center gap-1.5 text-[10px]">
                            <span class="text-slate-400">${p.official_caps}경기 ${p.official_goals}골</span>
                            <span class="${suit.isLow ? 'text-rose-400 font-bold' : 'text-emerald-400'}">· ${escapeHtml(suit.status)}</span>
                          </div>
                        </div>
                      ` : `
                        <span class="text-xs text-slate-500">비어 있음 (${escapeHtml(slot.label_ko)})</span>
                      `}
                    </div>
                    ${p ? `
                      <div class="flex items-center gap-1 shrink-0" onclick="event.stopPropagation()">
                        <button onclick="window.app.setCaptain(${p.id || p.player_id})"
                                title="주장(C) 지정"
                                class="px-1.5 py-1 rounded text-[10px] font-black ${isCap ? 'bg-amber-400 text-slate-950' : 'bg-slate-800 text-slate-400 hover:text-white'}">
                          C
                        </button>
                        <button onclick="window.app.startSwapSlot(${idx})"
                                title="다른 선수와 위치 바꾸기"
                                class="px-1.5 py-1 rounded bg-slate-800 hover:bg-sky-500 hover:text-slate-950 text-slate-300 text-[10px] font-bold">
                          ⇄
                        </button>
                        <button onclick="window.app.removePlayerFromSlot(${idx})"
                                title="배치 해제"
                                class="px-1.5 py-1 rounded bg-slate-800 hover:bg-rose-500 hover:text-white text-slate-400 text-[10px] font-bold">
                          ✕
                        </button>
                      </div>
                    ` : ''}
                  </div>
                `;
              }).join('')}
            </div>
          </div>
        </div>

        <!-- Column 3: Position Click A-Match Caps Recommendation & Direct Search Drawer (4 cols on lg) -->
        <div id="builder-candidate-drawer" class="lg:col-span-4 rounded-2xl bg-slate-900/95 border border-slate-800 p-4 space-y-3 shadow-xl">
          <div class="flex items-center justify-between border-b border-slate-800 pb-2.5">
            <div>
              <span class="text-[11px] font-bold text-amber-400 uppercase">
                ${isDirectSearching ? '🔍 직접 선수 검색 결과 (A매치 30회 이상)' : '🏅 포지션별 A매치 최다 출전 추천 (30회 이상)'}
              </span>
              <h3 class="text-base font-black text-white mt-0.5">
                ${focusedSlot ? `[${escapeHtml(focusedSlot.slot_code)}] ${escapeHtml(focusedSlot.label_ko)}` : '선수 후보 목록'}
                <span class="text-xs font-normal text-emerald-400 ml-1">
                  (${state.candSortBy === 'caps_desc' ? 'A매치 출전 경기 순' : '맞춤 정렬'} · ${candidates.length}명)
                </span>
              </h3>
            </div>
            <div class="flex items-center gap-1">
              <button onclick="window.app.showPositionRecommendedCaps()"
                      class="px-2.5 py-1 rounded-lg text-xs font-bold ${!isDirectSearching && state.candPosFilter === 'slot' ? 'bg-amber-400 text-slate-950 shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'}">
                🏅 포지션 추천 (출전순)
              </button>
              <button onclick="window.app.focusDirectPlayerSearch()"
                      class="px-2.5 py-1 rounded-lg text-xs font-bold ${isDirectSearching || state.candPosFilter === 'all' ? 'bg-sky-400 text-slate-950 shadow' : 'bg-slate-950 text-slate-400 border border-slate-800'}">
                🔍 직접 검색
              </button>
            </div>
          </div>

          <!-- Direct Search Input & Filter Controls -->
          <div class="space-y-2">
            <div class="relative">
              <input id="builder-cand-search-input"
                     type="text"
                     value="${escapeHtml(state.candSearch)}"
                     oninput="window.app.onCandSearch(this.value)"
                     placeholder="🔍 직접 선수 검색: 한글(영문) 이름 입력 (예: 펠레, Pelé, 호나우두...)"
                     class="w-full pl-3 pr-16 py-2.5 rounded-xl bg-slate-950 border ${isDirectSearching ? 'border-sky-400 ring-1 ring-sky-400/40' : 'border-slate-700'} text-xs sm:text-sm text-white placeholder-slate-400 focus:outline-none focus:border-amber-400" />
              ${isDirectSearching ? `
                <button onclick="window.app.onCandSearch('')"
                        class="absolute right-2 top-1/2 -translate-y-1/2 px-2 py-0.5 rounded bg-slate-800 hover:bg-slate-700 text-[11px] text-slate-300 font-bold">
                  초기화 ✕
                </button>
              ` : ''}
            </div>

            <div class="grid grid-cols-3 gap-1.5">
              <select onchange="window.app.onCandFilter('decade', this.value)"
                      class="px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200">
                <option value="all" ${state.candDecade === 'all' ? 'selected' : ''}>전체 시대</option>
                <option value="pre1960" ${state.candDecade === 'pre1960' ? 'selected' : ''}>1950년대 이전</option>
                <option value="1960s" ${state.candDecade === '1960s' ? 'selected' : ''}>1960년대</option>
                <option value="1970s" ${state.candDecade === '1970s' ? 'selected' : ''}>1970년대</option>
                <option value="1980s" ${state.candDecade === '1980s' ? 'selected' : ''}>1980년대</option>
                <option value="1990s" ${state.candDecade === '1990s' ? 'selected' : ''}>1990년대</option>
                <option value="2000s" ${state.candDecade === '2000s' ? 'selected' : ''}>2000년대</option>
                <option value="2010s" ${state.candDecade === '2010s' ? 'selected' : ''}>2010년대</option>
                <option value="2020s" ${state.candDecade === '2020s' ? 'selected' : ''}>2020년대</option>
              </select>

              <select onchange="window.app.onCandFilter('activeStatus', this.value)"
                      class="px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200">
                <option value="all" ${state.candActiveStatus === 'all' ? 'selected' : ''}>현역+은퇴 전체</option>
                <option value="retired" ${state.candActiveStatus === 'retired' ? 'selected' : ''}>은퇴 레전드</option>
                <option value="active" ${state.candActiveStatus === 'active' ? 'selected' : ''}>현역 선수</option>
              </select>

              <select onchange="window.app.onCandFilter('sortBy', this.value)"
                      class="px-2 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs font-bold text-amber-300">
                <option value="caps_desc" ${state.candSortBy === 'caps_desc' ? 'selected' : ''}>A매치 출전 경기 순</option>
                <option value="goals_desc" ${state.candSortBy === 'goals_desc' ? 'selected' : ''}>A매치 득점순</option>
                <option value="name_asc" ${state.candSortBy === 'name_asc' ? 'selected' : ''}>한글 이름순</option>
                <option value="debut_asc" ${state.candSortBy === 'debut_asc' ? 'selected' : ''}>데뷔 연도(과거순)</option>
                <option value="debut_desc" ${state.candSortBy === 'debut_desc' ? 'selected' : ''}>데뷔 연도(최신순)</option>
              </select>
            </div>

            <!-- Position quick filter pills -->
            <div class="flex items-center gap-1 overflow-x-auto pb-1">
              ${[
                { k: 'slot', l: `★ ${focusedSlot ? focusedSlot.slot_code : '포지션'} 맞춤 추천 (출전순)` },
                { k: 'all', l: '전체 포지션' },
                { k: 'GK', l: 'GK' },
                { k: 'DF', l: 'DF(수비)' },
                { k: 'MF', l: 'MF(미드필더)' },
                { k: 'FW', l: 'FW(공격)' }
              ].map(tab => `
                <button onclick="window.app.setCandPosFilter('${tab.k}')"
                        class="px-2.5 py-1 rounded-md text-[11px] font-bold whitespace-nowrap ${state.candPosFilter === tab.k && !isDirectSearching ? 'bg-emerald-500 text-slate-950' : 'bg-slate-950 text-slate-400 border border-slate-800'}">
                  ${escapeHtml(tab.l)}
                </button>
              `).join('')}
            </div>
          </div>

          <!-- Candidate Cards List (한글(영문) 기본 표기 + A매치 출전 경기 순 순위 표시) -->
          <div class="space-y-2 max-h-[580px] overflow-y-auto custom-scrollbar pr-1">
            ${candidates.length === 0 ? `
              <div class="py-12 text-center text-xs text-slate-400">
                조건에 맞는 후보가 없습니다. <button onclick="window.app.setCandPosFilter('all')" class="text-amber-400 underline font-bold">전체 포지션 보기</button>를 눌러보세요.
              </div>
            ` : candidates.map((p, rankIdx) => {
              const isAlreadyUsed = usedPlayerIds.has(p.id);
              const suit = focusedSlot ? computeClientSuitability(p, focusedSlot) : { status: '적합', isLow: false };
              let secPos = '';
              try {
                const arr = JSON.parse(p.secondary_positions || '[]');
                if (arr.length) secPos = ` / ${arr.join('·')}`;
              } catch (e) {}

              return `
                <div class="p-2.5 rounded-xl bg-slate-950/90 border ${isAlreadyUsed ? 'border-slate-800 opacity-60' : 'border-slate-800 hover:border-amber-400/60'} transition flex items-center justify-between gap-2.5">
                  <div class="flex items-center gap-2.5 min-w-0 flex-1 cursor-pointer" onclick="window.app.openPlayerModal(${p.id})">
                    ${renderPlayerAvatarHtml(p, country, 'w-11 h-11', 'text-xs')}
                    <div class="min-w-0 flex-1">
                      <div class="flex items-center gap-1.5 flex-wrap">
                        <span class="px-1.5 py-0.2 rounded bg-slate-800 text-[10px] font-black text-amber-400">#${rankIdx + 1}</span>
                        <span class="font-black text-xs sm:text-sm text-white truncate" title="${escapeHtml(formatNameKoEn(p))}">${escapeHtml(formatNameKoEn(p))}</span>
                        ${p.is_legend_test_case ? `<span class="px-1.5 py-0.2 rounded bg-amber-400/15 text-amber-300 border border-amber-400/30 text-[9px] font-bold">★레전드</span>` : ''}
                      </div>
                      <div class="flex items-center gap-2 text-[11px] text-slate-300 mt-0.5 flex-wrap">
                        <span class="px-1.5 py-0.2 rounded bg-emerald-500/20 text-emerald-300 font-black">A매치 ${p.official_caps}경기 (${p.official_goals}골)</span>
                        <span class="px-1.5 py-0.2 rounded bg-slate-800 text-amber-300 font-bold">${escapeHtml(p.primary_position)}${escapeHtml(secPos)}</span>
                        <span>${escapeHtml(p.active_period_label || '')}</span>
                      </div>
                      ${p.major_honors_ko ? `<div class="text-[10px] text-slate-400 truncate mt-0.5">🏆 ${escapeHtml(p.major_honors_ko)}</div>` : ''}
                    </div>
                  </div>

                  <div class="flex flex-col items-end gap-1 shrink-0">
                    <span class="text-[10px] px-1.5 py-0.5 rounded font-bold ${suit.isLow ? 'bg-rose-500/15 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'}">
                      ${escapeHtml(suit.status)}
                    </span>
                    ${isAlreadyUsed ? `
                      <span class="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400 text-[11px] font-bold cursor-not-allowed">
                        이미 배치됨
                      </span>
                    ` : `
                      <button onclick="window.app.assignPlayerToActiveSlot(${p.id})"
                              class="px-3 py-1 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs font-black transition">
                        + 배치
                      </button>
                    `}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================

  // ============================================================================
  // VIEW 2.5: SAVED BEST 11 GALLERY VIEW (Dedicated Tab)
  // ============================================================================
  function renderBoardView() {
    const filterCountry = state.boardCountryFilter || 'ALL';
    const search = (state.boardSearch || '').trim().toLowerCase();

    // Collect country stats for filter pills
    const countryMap = {};
    (state.savedLineups || []).forEach(l => {
      const snap = l.snapshot || {};
      const code = l.country_fifa_code || snap.country_fifa_code;
      const name = l.country_name_ko || snap.country_name_ko || code;
      const flag = snap.flag_emoji || (state.countries.find(c => c.fifa_code === code) || {}).flag_emoji || '⚽';
      if (code) {
        if (!countryMap[code]) countryMap[code] = { code, name, flag, count: 0 };
        countryMap[code].count++;
      }
    });

    const filteredLineups = (state.savedLineups || []).filter(l => {
      const snap = l.snapshot || {};
      const cCode = l.country_fifa_code || snap.country_fifa_code || '';
      if (filterCountry !== 'ALL' && cCode !== filterCountry) return false;
      if (search) {
        const teamName = (l.team_name || snap.team_name || '').toLowerCase();
        const countryName = (l.country_name_ko || snap.country_name_ko || '').toLowerCase();
        const fCode = (l.formation_code || snap.formation_code || '').toLowerCase();
        const players = snap.players || [];
        const playerNames = players.map(p => (p.name_ko || p.name_en || '').toLowerCase()).join(' ');
        if (!teamName.includes(search) && !countryName.includes(search) && !fCode.includes(search) && !playerNames.includes(search)) {
          return false;
        }
      }
      return true;
    });

    return `
      <div class="space-y-6">
        <!-- Hero Header -->
        <div class="rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-slate-950 border border-slate-800 p-6 sm:p-8 shadow-2xl relative overflow-hidden">
          <div class="absolute -right-10 -bottom-10 w-72 h-72 bg-amber-400/5 rounded-full blur-3xl pointer-events-none"></div>
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
            <div class="space-y-2">
              <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 text-xs font-bold">
                <span>📋 베스트 11 갤러리</span>
                <span>·</span>
                <span>총 ${filteredLineups.length}개 팀 (전체 ${state.savedLineups.length}개)</span>
              </div>
              <h2 class="text-2xl sm:text-3xl font-black text-white tracking-tight">
                저장된 역대 베스트 11 갤러리
              </h2>
              <p class="text-xs sm:text-sm text-slate-400 max-w-2xl leading-relaxed">
                사용자가 직접 구성하여 저장한 베스트11 및 국가별 공식 올타임 드림팀 목록입니다.<br class="hidden sm:inline" />
                전술판으로 즉시 불러와 수정하거나, 고해상도 PNG 완성 이미지 미리보기 및 새 탭 열기, 카카오톡 공유가 가능합니다.
              </p>
            </div>

            <div class="flex items-center gap-3 shrink-0 flex-wrap">
              <button onclick="window.app.navigate('builder')"
                      class="px-5 py-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs sm:text-sm shadow-lg shadow-amber-400/25 transition flex items-center gap-2">
                <span>⚽</span>
                <span>새 베스트11 만들기</span>
              </button>
              <button onclick="window.app.saveCurrentLineup(false)"
                      class="px-4 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs sm:text-sm shadow transition flex items-center gap-2">
                <span>💾</span>
                <span>현재 전술판 저장</span>
              </button>
            </div>
          </div>

          <!-- Country Filter Pills & Search Bar -->
          <div class="mt-6 pt-5 border-t border-slate-800/80 flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-center gap-1.5 overflow-x-auto custom-scrollbar pb-1 text-xs">
              <button onclick="window.app.setBoardCountryFilter('ALL')"
                      class="px-3 py-1.5 rounded-lg font-bold transition whitespace-nowrap ${filterCountry === 'ALL' ? 'bg-amber-400 text-slate-950 shadow' : 'bg-slate-800/90 text-slate-300 hover:bg-slate-700 hover:text-white'}">
                전체 (${state.savedLineups.length})
              </button>
              ${Object.values(countryMap).map(c => `
                <button onclick="window.app.setBoardCountryFilter('${c.code}')"
                        class="px-3 py-1.5 rounded-lg font-bold transition whitespace-nowrap flex items-center gap-1.5 ${filterCountry === c.code ? 'bg-amber-400 text-slate-950 shadow' : 'bg-slate-800/90 text-slate-300 hover:bg-slate-700 hover:text-white'}">
                  <span>${escapeHtml(c.flag)}</span>
                  <span>${escapeHtml(c.name)}</span>
                  <span class="text-[10px] px-1.5 py-0.2 rounded-full ${filterCountry === c.code ? 'bg-slate-950/20 text-slate-950' : 'bg-slate-900 text-slate-400'} font-mono">${c.count}</span>
                </button>
              `).join('')}
            </div>

            <!-- Search -->
            <div class="relative w-full md:w-72 shrink-0">
              <input type="text"
                     placeholder="팀명, 국가, 선수명 검색..."
                     value="${escapeHtml(state.boardSearch || '')}"
                     oninput="window.app.setBoardSearch(this.value)"
                     class="w-full bg-slate-950 border border-slate-700 rounded-xl px-3.5 py-2 pl-9 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400" />
              <span class="absolute left-3 top-2.5 text-slate-500 text-xs">🔍</span>
              ${state.boardSearch ? `
                <button onclick="window.app.setBoardSearch('');" class="absolute right-2.5 top-2 text-slate-400 hover:text-white text-xs">✕</button>
              ` : ''}
            </div>
          </div>
        </div>

        <!-- Cards Grid -->
        ${filteredLineups.length === 0 ? `
          <div class="rounded-3xl bg-slate-900/60 border border-slate-800 p-12 text-center space-y-4 shadow-xl">
            <div class="text-4xl">⚽</div>
            <h4 class="text-lg font-bold text-white">조건에 맞는 베스트 11이 없습니다</h4>
            <p class="text-xs text-slate-400">다른 국가를 선택하거나 검색어를 변경해 보세요.</p>
            <button onclick="window.app.setBoardCountryFilter('ALL'); window.app.setBoardSearch('');"
                    class="px-4 py-2 rounded-xl bg-amber-400 text-slate-950 font-bold text-xs shadow">
              전체 목록 보기
            </button>
          </div>
        ` : `
          <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
            ${filteredLineups.map((l) => {
              const snap = l.snapshot || {};
              const flag = snap.flag_emoji || (state.countries.find(c => c.fifa_code === l.country_fifa_code) || {}).flag_emoji || '⚽';
              const players = snap.players || [];
              const shareUrl = `${window.location.origin}/team/${l.share_slug}`;
              const teamTitle = l.team_name || snap.team_name || '올타임 베스트 11';
              const desc = l.team_description || snap.team_description || '';
              const cName = l.country_name_ko || snap.country_name_ko || l.country_fifa_code;
              const fCode = l.formation_code || snap.formation_code || '4-3-3';
              const style = l.tactical_style || snap.tactical_style || '균형형';

              return `
                <div class="rounded-2xl bg-slate-950 border border-slate-800/90 hover:border-amber-400/80 p-5 sm:p-6 flex flex-col justify-between gap-4 transition-all duration-200 shadow-xl group hover:-translate-y-0.5">
                  <div class="space-y-4">
                    <!-- Header: Country Flag, Title, Formation Badge & Style -->
                    <div class="flex items-start justify-between gap-3">
                      <div class="flex items-center gap-3.5 min-w-0">
                        <span class="text-3xl shrink-0 p-2 rounded-2xl bg-slate-900 border border-slate-800 shadow">${escapeHtml(flag)}</span>
                        <div class="min-w-0">
                          <h4 class="font-black text-white text-base sm:text-lg leading-tight truncate group-hover:text-amber-300 transition" title="${escapeHtml(teamTitle)}">
                            ${escapeHtml(teamTitle)}
                          </h4>
                          <div class="text-xs text-slate-400 font-medium mt-1 flex items-center gap-2 flex-wrap">
                            <span class="text-slate-200 font-bold">${escapeHtml(cName)}</span>
                            <span class="text-slate-600">·</span>
                            <span class="px-2 py-0.5 rounded-md bg-amber-400/10 border border-amber-400/30 text-xs font-black text-amber-300">포메이션 ${escapeHtml(fCode)}</span>
                          </div>
                        </div>
                      </div>
                      <span class="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-xs font-bold text-emerald-300 shrink-0">
                        ${escapeHtml(style)}
                      </span>
                    </div>

                    <!-- Team description if present -->
                    ${desc ? `
                      <div class="text-xs text-slate-300 leading-relaxed bg-slate-900/70 p-3 rounded-xl border border-slate-800/80">
                        ${escapeHtml(desc)}
                      </div>
                    ` : ''}

                    <!-- 11 Players Position-Line Squad Layout: Universal & 100% Squish-Proof on all PCs & Mobiles -->
                    <div class="rounded-2xl bg-slate-900/90 border border-slate-800 p-4 space-y-3 shadow-inner">
                      <div class="flex items-center justify-between pb-2 border-b border-slate-800/80">
                        <div class="flex items-center gap-2">
                          <span class="text-base">👥</span>
                          <span class="text-xs font-black text-slate-200">선발 11명 라인업 (포지션 라인별 명단)</span>
                        </div>
                        <span class="text-[11px] px-2 py-0.5 rounded-full bg-slate-800 text-amber-300 font-bold font-mono">${players.length}명 완비</span>
                      </div>

                      ${(() => {
                        const lines = { FW: [], MF: [], DF: [], GK: [] };
                        players.forEach(p => {
                          const pos = (p.slot_code || p.primary_position || 'XI').toUpperCase();
                          if (pos.startsWith('GK')) {
                            lines.GK.push(p);
                          } else if (pos.includes('B') || pos.includes('DF') || pos.includes('CB') || pos.includes('LB') || pos.includes('RB')) {
                            lines.DF.push(p);
                          } else if (pos.includes('M') || pos.includes('CM') || pos.includes('CAM') || pos.includes('CDM') || pos.includes('LM') || pos.includes('RM')) {
                            lines.MF.push(p);
                          } else {
                            lines.FW.push(p);
                          }
                        });

                        const renderLine = (label, linePlayers, badgeColor, textColor) => {
                          if (!linePlayers.length) return '';
                          return `
                            <div class="flex items-start gap-2.5 text-xs">
                              <span class="w-14 px-2 py-1 rounded-lg ${badgeColor} text-[11px] font-black text-center shrink-0 tracking-wider">${label}</span>
                              <div class="flex items-center gap-x-2 gap-y-1.5 flex-wrap text-slate-200 pt-0.5 font-medium">
                                ${linePlayers.map(p => `
                                  <span class="inline-flex items-center gap-1.5 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 hover:border-slate-700 shadow-sm transition">
                                    <strong class="text-slate-100 font-bold text-xs">${escapeHtml(formatPlayerSquadDisplayName(p.name_ko || p.name_en))}</strong>
                                    <span class="text-[10px] ${textColor} font-mono font-bold">(${escapeHtml(p.slot_code || p.primary_position || '')})</span>
                                    ${p.is_captain ? `<span class="text-[9px] px-1 rounded bg-amber-400 text-slate-950 font-black">C</span>` : ''}
                                  </span>
                                `).join('')}
                              </div>
                            </div>
                          `;
                        };

                        return [
                          renderLine('FW 공격', lines.FW, 'bg-rose-500/20 text-rose-300 border border-rose-500/40', 'text-rose-400'),
                          renderLine('MF 미드', lines.MF, 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40', 'text-emerald-400'),
                          renderLine('DF 수비', lines.DF, 'bg-sky-500/20 text-sky-300 border border-sky-500/40', 'text-sky-400'),
                          renderLine('GK 골키', lines.GK, 'bg-amber-500/20 text-amber-300 border border-amber-500/40', 'text-amber-400')
                        ].join('');
                      })()}
                    </div>
                  </div>

                  <!-- Clean action buttons row: fully spaced, never squished -->
                  <div class="pt-3.5 border-t border-slate-800/80 flex items-center justify-between gap-2 flex-wrap sm:flex-nowrap">
                    <div class="flex items-center gap-2 flex-1 min-w-0">
                      <button onclick="window.app.loadSavedLineupIntoBuilder('${escapeHtml(l.share_slug)}')"
                              class="flex-1 py-2 px-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs sm:text-sm transition flex items-center justify-center gap-1.5 shadow whitespace-nowrap">
                        <span>📂</span>
                        <span>전술판 불러오기</span>
                      </button>
                      <button onclick="window.app.openSavedLineupImagePreview('${escapeHtml(teamTitle)}', '${escapeHtml(l.share_slug)}')"
                              class="py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 font-bold text-xs sm:text-sm transition flex items-center justify-center gap-1.5 shadow whitespace-nowrap"
                              title="전술판 고해상도 완성 이미지 미리보기 & 새 탭에서 열기">
                        <span>🖼️</span>
                        <span>이미지 미리보기</span>
                      </button>
                    </div>
                    <div class="flex items-center gap-1.5 shrink-0">
                      <button onclick="window.app.copyShareUrl('${escapeHtml(shareUrl)}')"
                              class="py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 text-xs sm:text-sm font-bold transition flex items-center justify-center gap-1"
                              title="공유 링크 복사">
                        <span>🔗</span>
                        <span>링크</span>
                      </button>
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        `}
      </div>
    `;
  }

    // VIEW 3: AI VIRTUAL MATCHUP ARENA (Section 7)
  // ============================================================================
  function renderArenaView() {
    return `
      <div class="py-24 text-center max-w-lg mx-auto">
        <div class="w-16 h-16 mx-auto mb-4 rounded-2xl bg-amber-400/10 border border-amber-400/30 flex items-center justify-center text-3xl">
          ⚽
        </div>
        <h2 class="text-xl font-black text-white mb-2">AI 가상 대결 기능이 비활성화되었습니다</h2>
        <p class="text-slate-400 text-sm leading-relaxed mb-6">
          현재 ALL-TIME XI는 30개국 레전드 선수를 기반으로 한 <strong>베스트11 전술판 제작·공유 및 고해상도 PNG 저장</strong>에 집중하고 있습니다.
        </p>
        <button onclick="window.app.navigate('builder')" class="px-5 py-3 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-sm transition">
          ⚽ 베스트11 만들기로 이동
        </button>
      </div>
    `;
    const teamAObj = state.savedLineups.find(l => l.share_slug === state.arenaTeamASlug);
    const teamBObj = state.savedLineups.find(l => l.share_slug === state.arenaTeamBSlug);
    const snapA = teamAObj ? teamAObj.snapshot : null;
    const snapB = teamBObj ? teamBObj.snapshot : null;

    const renderMiniTeamPreview = (snap) => {
      if (!snap) return `<div class="p-8 text-center text-slate-500 text-xs">팀을 선택하세요</div>`;
      const slots = (snap.players || []).map(p => ({
        slot_index: p.slot_index,
        slot_code: p.slot_code,
        label_ko: p.slot_label_ko || p.slot_code,
        x: p.x,
        y: p.y,
        player: p,
        is_captain: p.is_captain,
        suitability: { status: p.suitability_status || '적합', isLow: (p.suitability_status || '').includes('낮음') }
      }));
      return `
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs px-1">
            <span class="font-bold text-slate-300">${escapeHtml(snap.flag_emoji || '')} ${escapeHtml(snap.country_name_ko)} · 포메이션 ${escapeHtml(snap.formation_code)}</span>
            <span class="text-amber-400 font-semibold">전술: ${escapeHtml(snap.tactical_style)}</span>
          </div>
          ${renderTacticalPitchHtml({ slots, country: snap, themeId: snap.board_color_theme || 'classic_emerald', interactive: false, compact: true })}
        </div>
      `;
    };

    const res = state.arenaResult;
    const an = res ? res.analysis : null;

    return `
      <div class="space-y-6">
        <!-- Arena Header -->
        <div class="rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/70 border border-slate-800 p-5 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span class="text-xs font-black uppercase tracking-wider text-amber-400">AI DREAM MATCH SIMULATOR</span>
            <h1 class="text-2xl sm:text-3xl font-black text-white mt-0.5">AI 베스트11 가상 대결</h1>
            <p class="text-xs sm:text-sm text-slate-300 mt-1">
              서로 다른 국가 또는 같은 국가의 시대별 드림팀을 선택해 전성기 기량·전술 조화·포지션 상성을 Gemini AI로 정밀 비교합니다.
            </p>
          </div>
          <div class="flex items-center gap-2">
            <span class="px-3.5 py-2 rounded-xl text-xs font-bold bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 flex items-center gap-1.5">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              AI 전술 엔진 활성화됨
            </span>
            <button onclick="window.app.navigate('builder')"
                    class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold border border-slate-700">
              + 새 드림팀 만들기
            </button>
          </div>
        </div>

        <!-- Team A vs Team B Selector -->
        <div class="grid grid-cols-1 lg:grid-cols-11 gap-4 items-start">
          <!-- TEAM A -->
          <div class="lg:col-span-5 rounded-2xl bg-slate-900/90 border border-slate-800 p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-0.5 rounded bg-amber-400 text-slate-950 text-xs font-black">TEAM A (홈 드림팀)</span>
              <select onchange="window.app.setArenaTeam('A', this.value)"
                      class="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm font-bold text-white max-w-[260px]">
                ${state.savedLineups.map(l => `
                  <option value="${escapeHtml(l.share_slug)}" ${l.share_slug === state.arenaTeamASlug ? 'selected' : ''}>
                    [${escapeHtml(l.country_name_ko)}] ${escapeHtml(l.team_name)} (${escapeHtml(l.formation_code)})
                  </option>
                `).join('')}
              </select>
            </div>
            ${renderMiniTeamPreview(snapA)}
          </div>

          <!-- Center VS Trigger -->
          <div class="lg:col-span-1 flex flex-col items-center justify-center py-4 lg:py-24 gap-3">
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-amber-400 to-emerald-500 text-slate-950 font-black text-2xl flex items-center justify-center shadow-2xl">
              VS
            </div>
            <select onchange="window.app.setArenaProvider(this.value)"
                    class="px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-slate-200 font-bold">
              <option value="engine" ${(!state.arenaProvider || state.arenaProvider === 'engine') ? 'selected' : ''}>전술 분석 AI (자체 탑재)</option>
              ${state.aiStatus?.providers?.gemini?.configured ? `<option value="gemini" ${state.arenaProvider === 'gemini' ? 'selected' : ''}>Gemini AI</option>` : ''}
              ${state.aiStatus?.providers?.openai?.configured ? `<option value="openai" ${state.arenaProvider === 'openai' ? 'selected' : ''}>OpenAI</option>` : ''}
            </select>
            <button onclick="window.app.runArenaComparison()"
                    ${state.arenaLoading ? 'disabled' : ''}
                    class="w-full lg:w-auto px-4 py-3 rounded-xl bg-amber-400 hover:bg-amber-300 disabled:opacity-50 text-slate-950 font-black text-xs sm:text-sm shadow-xl shadow-amber-400/20 transition whitespace-nowrap">
              ${state.arenaLoading ? '⏳ AI 분석 중...' : '⚡ AI 대결 시작'}
            </button>
          </div>

          <!-- TEAM B -->
          <div class="lg:col-span-5 rounded-2xl bg-slate-900/90 border border-slate-800 p-4 space-y-3">
            <div class="flex items-center justify-between">
              <span class="px-2.5 py-0.5 rounded bg-sky-400 text-slate-950 text-xs font-black">TEAM B (어웨이 드림팀)</span>
              <select onchange="window.app.setArenaTeam('B', this.value)"
                      class="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm font-bold text-white max-w-[260px]">
                ${state.savedLineups.map(l => `
                  <option value="${escapeHtml(l.share_slug)}" ${l.share_slug === state.arenaTeamBSlug ? 'selected' : ''}>
                    [${escapeHtml(l.country_name_ko)}] ${escapeHtml(l.team_name)} (${escapeHtml(l.formation_code)})
                  </option>
                `).join('')}
              </select>
            </div>
            ${renderMiniTeamPreview(snapB)}
          </div>
        </div>

        <!-- AI Analysis Output Section (Section 7-4: 결과 1~6) -->
        ${an ? `
          <div id="ai-analysis-report" class="space-y-6 pt-4">
            <!-- Share & PNG Export Bar for AI Result (Section 7-5) -->
            <div class="rounded-2xl bg-emerald-950/70 border border-emerald-500/50 p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
              <div>
                <div class="text-xs font-bold text-emerald-300">
                  AI 전술 분석 완료 (${escapeHtml(res.provider.toUpperCase())} · ${escapeHtml(res.model)})
                </div>
                <div class="text-xs text-slate-300 mt-0.5">
                  공유 링크: <code class="px-2 py-0.5 rounded bg-slate-950 text-amber-300 font-mono">${escapeHtml(window.location.origin + '/match/' + res.share_slug)}</code>
                </div>
              </div>
              <div class="flex flex-wrap items-center gap-2">
                <button onclick="window.app.copyShareUrl('${escapeHtml(window.location.origin + '/match/' + res.share_slug)}')"
                        class="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-white border border-slate-700 text-xs font-bold">
                  🔗 분석 결과 URL 복사
                </button>
                <a href="/api/ai/comparisons/${escapeHtml(res.share_slug)}/png" download
                   class="px-3.5 py-1.5 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs font-black">
                  🖼️ VS 전술판 분석 이미지(PNG) 저장
                </a>
              </div>
            </div>

            <!-- 결과 1. 예상 승부 -->
            <div class="rounded-3xl bg-slate-900/95 border border-slate-800 p-6 text-center space-y-3 shadow-2xl">
              <span class="px-3 py-1 rounded-full bg-amber-400/15 text-amber-300 border border-amber-400/30 text-xs font-black">
                결과 1 · AI 가상 경기 예상 승부
              </span>
              <div class="flex flex-col sm:flex-row items-center justify-center gap-4 sm:gap-8 py-2">
                <div class="text-right">
                  <div class="text-lg sm:text-2xl font-black text-white">${escapeHtml(an.expected_outcome.team_a_name)}</div>
                  <div class="text-xs text-amber-400">${escapeHtml(res.team_a.country_name_ko)} · ${escapeHtml(res.team_a.formation_code)}</div>
                </div>
                <div class="px-6 py-3 rounded-2xl bg-slate-950 border-2 border-amber-400/60 text-3xl sm:text-5xl font-black text-amber-400 tracking-wider">
                  ${an.expected_outcome.team_a_goals} : ${an.expected_outcome.team_b_goals}
                </div>
                <div class="text-left">
                  <div class="text-lg sm:text-2xl font-black text-white">${escapeHtml(an.expected_outcome.team_b_name)}</div>
                  <div class="text-xs text-sky-400">${escapeHtml(res.team_b.country_name_ko)} · ${escapeHtml(res.team_b.formation_code)}</div>
                </div>
              </div>
              <div class="text-sm sm:text-base font-bold text-emerald-300">${escapeHtml(an.expected_outcome.win_tendency_ko)}</div>
              <p class="text-xs text-slate-400 max-w-2xl mx-auto bg-slate-950/70 px-4 py-2 rounded-xl border border-slate-800">
                ℹ️ ${escapeHtml(an.expected_outcome.scenario_disclaimer_ko)}
              </p>
            </div>

            <!-- 결과 2. 전력 비교 (6대 항목) -->
            <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-4">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <h3 class="text-lg font-black text-white">결과 2 · 부문별 전력 비교 (전성기 기량 및 현대 전술 환경 공통 가정)</h3>
                <span class="text-xs text-slate-400">${escapeHtml(an.power_comparison_note_ko)}</span>
              </div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                ${(an.power_comparison || []).map(cat => {
                  const a = Number(cat.team_a_score) || 85;
                  const b = Number(cat.team_b_score) || 85;
                  const aPct = Math.round((a / (a + b)) * 100);
                  return `
                    <div class="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2">
                      <div class="flex items-center justify-between text-sm font-black">
                        <span class="text-amber-400">${a}점</span>
                        <span class="text-white">${escapeHtml(cat.category_name_ko)}</span>
                        <span class="text-sky-400">${b}점</span>
                      </div>
                      <div class="w-full h-2.5 rounded-full bg-slate-800 overflow-hidden flex">
                        <div class="bg-amber-400 h-full" style="width:${aPct}%"></div>
                        <div class="bg-sky-400 h-full" style="width:${100 - aPct}%"></div>
                      </div>
                      <div class="text-[11px] text-slate-400"><strong>평가 기준:</strong> ${escapeHtml(cat.evaluation_criteria_ko)}</div>
                      <p class="text-xs text-slate-200 leading-relaxed">${escapeHtml(cat.rationale_ko)}</p>
                    </div>
                  `;
                }).join('')}
              </div>
            </div>

            <!-- 결과 3. 핵심 맞대결 TOP 3 -->
            <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-4">
              <h3 class="text-lg font-black text-white border-b border-slate-800 pb-3">결과 3 · 승부를 좌우할 핵심 포지션 맞대결 TOP 3</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                ${(an.key_matchups || []).map((km, idx) => `
                  <div class="p-4 rounded-xl bg-slate-950/90 border border-slate-800 space-y-2.5 flex flex-col justify-between">
                    <div class="space-y-2">
                      <span class="px-2 py-0.5 rounded bg-amber-400/15 text-amber-300 text-[11px] font-black">MATCHUP #${idx + 1}</span>
                      <h4 class="font-black text-sm text-white">${escapeHtml(km.matchup_title_ko)}</h4>
                      <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 text-xs space-y-1">
                        <div class="text-amber-300 font-bold">🅰️ ${escapeHtml(km.team_a_player_ko)}</div>
                        <div class="text-center text-[10px] text-slate-500 font-black">VS</div>
                        <div class="text-sky-300 font-bold">🅱️ ${escapeHtml(km.team_b_player_ko)}</div>
                      </div>
                      <p class="text-xs text-slate-300 leading-relaxed">${escapeHtml(km.tactical_importance_ko)}</p>
                    </div>
                    <div class="pt-2 border-t border-slate-800 text-xs font-bold text-emerald-400">
                      ⚖️ 상성 평가: ${escapeHtml(km.expected_edge_ko)}
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- 결과 4. 승부를 가르는 결정적 요인 & 결과 5. 예상 경기 흐름 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
              <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
                <h3 class="text-lg font-black text-white border-b border-slate-800 pb-2.5">결과 4 · 양 팀 강점·약점 및 결정적 요인</h3>
                <div class="space-y-3 text-xs">
                  <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
                    <div class="font-black text-amber-400 text-sm">${escapeHtml(an.expected_outcome.team_a_name)}</div>
                    <div class="text-emerald-300"><strong>강점:</strong> ${(an.decisive_factors.team_a.strengths_ko || []).map(escapeHtml).join(' / ')}</div>
                    <div class="text-rose-300"><strong>약점·리스크:</strong> ${(an.decisive_factors.team_a.weaknesses_ko || []).map(escapeHtml).join(' / ')}</div>
                  </div>
                  <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5">
                    <div class="font-black text-sky-400 text-sm">${escapeHtml(an.expected_outcome.team_b_name)}</div>
                    <div class="text-emerald-300"><strong>강점:</strong> ${(an.decisive_factors.team_b.strengths_ko || []).map(escapeHtml).join(' / ')}</div>
                    <div class="text-rose-300"><strong>약점·리스크:</strong> ${(an.decisive_factors.team_b.weaknesses_ko || []).map(escapeHtml).join(' / ')}</div>
                  </div>
                  <div class="p-3 rounded-xl bg-amber-400/10 border border-amber-400/30 text-amber-100 leading-relaxed">
                    <strong>🎯 승부의 분수령:</strong> ${escapeHtml(an.decisive_factors.decisive_turning_point_ko)}
                  </div>
                </div>
              </div>

              <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
                <h3 class="text-lg font-black text-white border-b border-slate-800 pb-2.5">결과 5 · 전·후반 예상 경기 흐름</h3>
                <div class="space-y-3 text-xs leading-relaxed">
                  <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                    <div class="font-black text-amber-400 text-sm">⏱️ 전반전 (1st Half) 전술 흐름</div>
                    <p class="text-slate-200">${escapeHtml(an.expected_match_flow.first_half_ko)}</p>
                  </div>
                  <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                    <div class="font-black text-sky-400 text-sm">⏱️ 후반전 (2nd Half) 승부처 흐름</div>
                    <p class="text-slate-200">${escapeHtml(an.expected_match_flow.second_half_ko)}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- 결과 6. AI 최종 판정 및 사실/가정 구분 -->
            <div class="rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-amber-950/30 border-2 border-amber-400/50 p-6 space-y-4">
              <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="px-3 py-1 rounded-full bg-amber-400 text-slate-950 text-xs font-black">결과 6 · AI 최종 판정</span>
                <span class="text-base sm:text-xl font-black text-amber-300">🏆 최종 우세 판정: ${escapeHtml(an.final_verdict.winner_team_ko)}</span>
              </div>
              <p class="text-sm sm:text-base text-white font-semibold leading-relaxed">${escapeHtml(an.final_verdict.final_summary_ko)}</p>
              <ul class="space-y-1 text-xs text-slate-200 list-disc list-inside">
                ${(an.final_verdict.core_reasons_ko || []).map(r => `<li>${escapeHtml(r)}</li>`).join('')}
              </ul>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-3 border-t border-slate-800 text-xs">
                <div class="p-3 rounded-xl bg-slate-950/90 border border-emerald-500/30">
                  <div class="font-black text-emerald-400 mb-1">📊 분석에 반영된 객관적 사실 (공식 기록)</div>
                  <ul class="list-disc list-inside space-y-1 text-slate-300">
                    ${(an.final_verdict.verified_facts_used_ko || []).map(f => `<li>${escapeHtml(f)}</li>`).join('')}
                  </ul>
                </div>
                <div class="p-3 rounded-xl bg-slate-950/90 border border-sky-500/30">
                  <div class="font-black text-sky-400 mb-1">🧪 전술 시뮬레이션 가정 및 한계</div>
                  <ul class="list-disc list-inside space-y-1 text-slate-300">
                    ${(an.final_verdict.tactical_assumptions_used_ko || []).map(a => `<li>${escapeHtml(a)}</li>`).join('')}
                  </ul>
                </div>
              </div>
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  // ============================================================================
  // VIEW 4: HISTORICAL PLAYER DATABASE EXPLORER (Section 8)
  // ============================================================================
  function renderDatabaseView() {
    return `
      <div class="space-y-5">
        <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-4">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div>
              <span class="text-xs font-black uppercase text-emerald-400">HISTORICAL NATIONAL TEAM ARCHIVE</span>
              <h1 class="text-2xl font-black text-white">역대 국가대표 선수 데이터베이스 (A매치 30회 이상)</h1>
              <p class="text-xs sm:text-sm text-slate-400 mt-0.5">
                1900년대~2020년대 30개국 성인 남자 A대표팀 공식 경기 30회 이상 출전 선수 3,817명을 출전 순위·득점 순위·포지션·활동 시대별로 탐색합니다.
              </p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="window.app.startCountryBuilder(state.dbCountryCode === 'ALL' ? 'BRA' : state.dbCountryCode)"
                      class="px-4 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 text-xs sm:text-sm font-black">
                ⚽ 이 국가 베스트11 만들기 →
              </button>
            </div>
          </div>

          <!-- Filter Bar -->
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-2.5 pt-2">
            <select onchange="window.app.onDbFilter('country', this.value)"
                    class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm font-bold text-white">
              <option value="ALL" ${state.dbCountryCode === 'ALL' ? 'selected' : ''}>🌍 30개국 전체 보기</option>
              ${state.countries.map(c => `
                <option value="${escapeHtml(c.fifa_code)}" ${c.fifa_code === state.dbCountryCode ? 'selected' : ''}>
                  #${c.fifa_rank} ${escapeHtml(c.flag_emoji)} ${escapeHtml(c.name_ko)} (${c.eligible_player_count}명)
                </option>
              `).join('')}
            </select>

            <input type="text"
                   value="${escapeHtml(state.dbSearch)}"
                   oninput="window.app.onDbFilter('search', this.value)"
                   placeholder="선수 이름·영문·별칭·소속클럽 검색..."
                   class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white placeholder-slate-500" />

            <select onchange="window.app.onDbFilter('position', this.value)"
                    class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white">
              <option value="all" ${state.dbPosition === 'all' ? 'selected' : ''}>포지션 전체</option>
              <option value="GK" ${state.dbPosition === 'GK' ? 'selected' : ''}>GK (골키퍼)</option>
              <option value="DF" ${state.dbPosition === 'DF' ? 'selected' : ''}>DF (수비수)</option>
              <option value="MF" ${state.dbPosition === 'MF' ? 'selected' : ''}>MF (미드필더)</option>
              <option value="FW" ${state.dbPosition === 'FW' ? 'selected' : ''}>FW (공격수)</option>
            </select>

            <select onchange="window.app.onDbFilter('decade', this.value)"
                    class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white">
              <option value="all" ${state.dbDecade === 'all' ? 'selected' : ''}>활동 시대 전체</option>
              <option value="1930s" ${state.dbDecade === '1930s' ? 'selected' : ''}>1930년대</option>
              <option value="1940s" ${state.dbDecade === '1940s' ? 'selected' : ''}>1940년대</option>
              <option value="1950s" ${state.dbDecade === '1950s' ? 'selected' : ''}>1950년대</option>
              <option value="1960s" ${state.dbDecade === '1960s' ? 'selected' : ''}>1960년대</option>
              <option value="1970s" ${state.dbDecade === '1970s' ? 'selected' : ''}>1970년대</option>
              <option value="1980s" ${state.dbDecade === '1980s' ? 'selected' : ''}>1980년대</option>
              <option value="1990s" ${state.dbDecade === '1990s' ? 'selected' : ''}>1990년대</option>
              <option value="2000s" ${state.dbDecade === '2000s' ? 'selected' : ''}>2000년대</option>
              <option value="2010s" ${state.dbDecade === '2010s' ? 'selected' : ''}>2010년대</option>
              <option value="2020s" ${state.dbDecade === '2020s' ? 'selected' : ''}>2020년대</option>
            </select>

            <select onchange="window.app.onDbFilter('activeStatus', this.value)"
                    class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white">
              <option value="all" ${state.dbActiveStatus === 'all' ? 'selected' : ''}>현역 + 은퇴 전체</option>
              <option value="retired" ${state.dbActiveStatus === 'retired' ? 'selected' : ''}>은퇴 선수</option>
              <option value="active" ${state.dbActiveStatus === 'active' ? 'selected' : ''}>현역 선수</option>
            </select>

            <select onchange="window.app.onDbFilter('sortBy', this.value)"
                    class="px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-xs sm:text-sm text-white font-bold">
              <option value="caps_desc" ${state.dbSortBy === 'caps_desc' ? 'selected' : ''}>정렬: 역대 A매치 출전 순위</option>
              <option value="goals_desc" ${state.dbSortBy === 'goals_desc' ? 'selected' : ''}>정렬: 역대 A매치 득점 순위</option>
              <option value="name_asc" ${state.dbSortBy === 'name_asc' ? 'selected' : ''}>정렬: 이름순</option>
              <option value="debut_asc" ${state.dbSortBy === 'debut_asc' ? 'selected' : ''}>정렬: 데뷔 연도(과거순)</option>
              <option value="debut_desc" ${state.dbSortBy === 'debut_desc' ? 'selected' : ''}>정렬: 데뷔 연도(최신순)</option>
            </select>
          </div>
        </div>

        <!-- Players Cards Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3.5">
          ${state.dbPlayers.map((p, idx) => {
            const cObj = state.countries.find(c => c.fifa_code === p.represented_fifa_code) || {};
            return `
              <div onclick="window.app.openPlayerModal(${p.id})"
                   class="rounded-2xl bg-slate-900/90 hover:bg-slate-800/90 border border-slate-800 hover:border-amber-400/60 p-4 cursor-pointer transition flex flex-col justify-between gap-3 shadow">
                <div class="flex items-start gap-3">
                  ${renderPlayerAvatarHtml(p, cObj, 'w-14 h-14', 'text-base')}
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center justify-between gap-1">
                      <span class="text-[11px] font-bold text-slate-400">#${idx + 1} · ${escapeHtml(p.flag_emoji || '')} ${escapeHtml(p.country_name_ko)}</span>
                      <span class="px-2 py-0.5 rounded bg-slate-950 border border-slate-700 text-[11px] font-black text-amber-400">${escapeHtml(p.primary_position)}</span>
                    </div>
                    <div class="font-black text-base text-white truncate mt-0.5" title="${escapeHtml(formatNameKoEn(p))}">${escapeHtml(formatNameKoEn(p))}</div>
                    <div class="flex items-center gap-2 mt-1.5 text-xs">
                      <span class="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 font-black">${p.official_caps}경기 ${p.official_goals}골</span>
                      <span class="text-slate-400">${escapeHtml(p.active_period_label || '')}</span>
                    </div>
                  </div>
                </div>
                <div class="pt-2.5 border-t border-slate-800/80 text-[11px] text-slate-300 space-y-1">
                  ${p.major_clubs_ko ? `<div class="truncate">🏟️ <strong>주요 클럽:</strong> ${escapeHtml(p.major_clubs_ko)}</div>` : ''}
                  ${p.major_honors_ko ? `<div class="truncate text-amber-300/90">🏆 ${escapeHtml(p.major_honors_ko)}</div>` : `<div class="truncate text-slate-400">${escapeHtml(p.play_style_ko || '')}</div>`}
                  <div class="flex items-center justify-between text-[10px] text-slate-500 pt-1">
                    <span>출처: ${escapeHtml(p.record_source_name)}</span>
                    <span class="text-amber-400 font-bold">상세 프로필 →</span>
                  </div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;
  }

  // ============================================================================
  // VIEW 5: DATA QUALITY, COVERAGE & SOURCES REPORT (Section 3-5)
  // ============================================================================
  function renderQualityView() {
    const rep = state.qualityReport;
    if (!rep) {
      return `<div class="py-16 text-center text-slate-400">데이터 품질 리포트를 불러오는 중입니다...</div>`;
    }
    const sum = rep.summary;
    const decEntries = Object.entries(sum.global_decade_distribution || {});
    const maxDecVal = Math.max(1, ...decEntries.map(([, v]) => v));

    return `
      <div class="space-y-6">
        <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-6 space-y-3">
          <span class="text-xs font-black uppercase text-emerald-400">DATA ENGINEERING & VERIFICATION REPORT</span>
          <h1 class="text-2xl sm:text-3xl font-black text-white">데이터 품질 검사 · 시대별 분포 · 출처 검증</h1>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">${escapeHtml(sum.data_scope_statement_ko)}</p>

          <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-2">
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div class="text-2xl font-black text-amber-400">${sum.total_countries}개국</div>
              <div class="text-xs text-slate-400">FIFA Top 30 대상국</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div class="text-2xl font-black text-emerald-400">${sum.total_eligible_30_caps_players.toLocaleString()}명</div>
              <div class="text-xs text-slate-400">A매치 30회+ 검증 선수</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div class="text-2xl font-black text-sky-400">${sum.legends_test_set_verified_count}명 전수 확인</div>
              <div class="text-xs text-slate-400">필수 전설 테스트 세트</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div class="text-2xl font-black text-purple-400">${sum.overall_photo_coverage_pct}%</div>
              <div class="text-xs text-slate-400">선수 사진 확보율 (+대체 아바타 100%)</div>
            </div>
            <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <div class="text-2xl font-black text-rose-400">${sum.total_caps_discrepancy_flags}건</div>
              <div class="text-xs text-slate-400">출처 간 출전수 차이 주석 관리</div>
            </div>
          </div>
        </div>

        <!-- Global Era Distribution Bar Chart -->
        <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-4">
          <h2 class="text-lg font-black text-white">전체 선수 시대별 분포 (1900년대 ~ 2020년대)</h2>
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-13 gap-2 items-end pt-2">
            ${decEntries.map(([dec, cnt]) => {
              const hPct = Math.max(12, Math.round((cnt / maxDecVal) * 120));
              return `
                <div class="flex flex-col items-center p-2 rounded-xl bg-slate-950 border border-slate-800">
                  <span class="text-xs font-black text-amber-400 mb-1">${cnt}명</span>
                  <div class="w-full bg-slate-900 rounded h-28 flex items-end justify-center p-1">
                    <div class="w-full rounded bg-gradient-to-t from-emerald-600 to-amber-400" style="height:${hPct}px"></div>
                  </div>
                  <span class="text-[11px] font-bold text-slate-300 mt-1.5">${escapeHtml(dec)}</span>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Country-by-Country Quality Table -->
        <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3 overflow-x-auto">
          <h2 class="text-lg font-black text-white">국가별 A매치 30회 이상 등록 선수 및 시대·포지션 분포</h2>
          <table class="w-full text-left border-collapse text-xs">
            <thead>
              <tr class="border-b border-slate-800 text-slate-400">
                <th class="py-2.5 px-2">순위</th>
                <th class="py-2.5 px-2">국가</th>
                <th class="py-2.5 px-2">30회+ 선수</th>
                <th class="py-2.5 px-2">2000년 이전 레전드</th>
                <th class="py-2.5 px-2">포지션 (GK/DF/MF/FW)</th>
                <th class="py-2.5 px-2">사진 확보율</th>
                <th class="py-2.5 px-2">출처 차이 주석</th>
                <th class="py-2.5 px-2">최종 갱신일</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60">
              ${rep.country_statistics.map(cs => `
                <tr class="hover:bg-slate-800/50">
                  <td class="py-2 px-2 font-black text-amber-400">#${cs.fifa_rank}</td>
                  <td class="py-2 px-2 font-bold text-white">${escapeHtml(cs.flag_emoji)} ${escapeHtml(cs.name_ko)} (${escapeHtml(cs.fifa_code)})</td>
                  <td class="py-2 px-2 font-black text-emerald-400">${cs.eligible_30_caps_players}명</td>
                  <td class="py-2 px-2 text-sky-300 font-semibold">${cs.pre_2000_players_count}명</td>
                  <td class="py-2 px-2 text-slate-300">
                    GK ${cs.position_counts.GK || 0} · DF ${cs.position_counts.DF || 0} · MF ${cs.position_counts.MF || 0} · FW ${cs.position_counts.FW || 0}
                  </td>
                  <td class="py-2 px-2 text-slate-300">${cs.photo_coverage_rate_pct}%</td>
                  <td class="py-2 px-2 text-slate-400">${cs.caps_discrepancy_count}건</td>
                  <td class="py-2 px-2 text-slate-400">${escapeHtml(cs.last_updated_date)}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>

        <!-- Historical Succession Policies & Data Sources -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
            <h3 class="text-base font-black text-white">역대 국가대표팀 기록 승계 정책 (Section 3-2)</h3>
            <div class="space-y-2.5 text-xs">
              ${rep.succession_policies.map(sp => `
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="font-black text-amber-400">${escapeHtml(sp.historical_team_name_ko)}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold ${sp.is_auto_merged ? 'bg-emerald-500/20 text-emerald-300' : 'bg-rose-500/20 text-rose-300'}">
                      ${escapeHtml(sp.policy_rule_ko)}
                    </span>
                  </div>
                  <p class="text-slate-300 leading-relaxed">${escapeHtml(sp.fifa_recognition_note_ko)}</p>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
            <h3 class="text-base font-black text-white">활용 데이터 출처 및 라이선스 명세 (Section 3-1)</h3>
            <div class="space-y-2.5 text-xs">
              ${rep.data_sources.map(ds => `
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="font-black text-sky-400">${escapeHtml(ds.source_name)}</span>
                    <span class="text-slate-400">갱신: ${escapeHtml(ds.last_updated_date)}</span>
                  </div>
                  <p class="text-slate-300">${escapeHtml(ds.coverage_scope_ko)}</p>
                  <p class="text-[11px] text-slate-400">라이선스: ${escapeHtml(ds.terms_and_license_ko)}</p>
                </div>
              `).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // VIEW 6: ADMIN CONSOLE (Section 12)
  // ============================================================================
  function renderAdminView() {
    return `
      <div class="space-y-6">
        <div class="rounded-2xl bg-slate-900 border border-amber-500/40 p-5 flex items-center justify-between">
          <div>
            <span class="text-xs font-black text-amber-400 uppercase">ADMINISTRATION CONSOLE</span>
            <h1 class="text-2xl font-black text-white">관리자 데이터 관리 및 품질 검수 콘솔</h1>
            <p class="text-xs text-slate-400">선수 추가·수정, A매치 출전 기록 수정, 중복 선수 병합, CSV 일괄 가져오기, FIFA 랭킹 스냅샷 갱신 및 수정 이력을 관리합니다.</p>
          </div>
          <button onclick="window.app.navigate('home')" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold">
            일반 화면으로 돌아가기
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
          <!-- Add / Update Player Form -->
          <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
            <h3 class="text-base font-black text-amber-400">1. 선수 데이터 및 A매치 기록 추가/수정</h3>
            <div class="grid grid-cols-2 gap-2.5 text-xs">
              <div>
                <label class="block text-slate-400 mb-1">국가 코드 (FIFA)</label>
                <select id="adm-country" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white">
                  ${state.countries.map(c => `<option value="${c.fifa_code}">${c.name_ko} (${c.fifa_code})</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block text-slate-400 mb-1">수정할 선수 ID (신규면 비워둠)</label>
                <input id="adm-pid" type="number" placeholder="신규 등록 시 공란" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
              <div>
                <label class="block text-slate-400 mb-1">한국어 이름 *</label>
                <input id="adm-name-ko" type="text" placeholder="예: 지쿠" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
              <div>
                <label class="block text-slate-400 mb-1">영어 이름 *</label>
                <input id="adm-name-en" type="text" placeholder="예: Zico" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
              <div>
                <label class="block text-slate-400 mb-1">주 포지션 *</label>
                <select id="adm-pos" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white">
                  ${['GK', 'CB', 'LB', 'RB', 'CDM', 'CM', 'CAM', 'LW', 'RW', 'ST'].map(p => `<option value="${p}">${p}</option>`).join('')}
                </select>
              </div>
              <div>
                <label class="block text-slate-400 mb-1">공식 A매치 출전 횟수 *</label>
                <input id="adm-caps" type="number" value="35" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
              <div>
                <label class="block text-slate-400 mb-1">공식 A매치 득점 *</label>
                <input id="adm-goals" type="number" value="10" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
              <div>
                <label class="block text-slate-400 mb-1">대표팀 활동 연도 (시작~종료)</label>
                <div class="flex gap-1">
                  <input id="adm-y1" type="number" value="1998" class="w-1/2 px-2 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                  <input id="adm-y2" type="number" value="2010" class="w-1/2 px-2 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                </div>
              </div>
              <div class="col-span-2">
                <label class="block text-slate-400 mb-1">사진 URL 및 라이선스 정보</label>
                <div class="flex gap-2">
                  <input id="adm-img" type="text" placeholder="https://commons.wikimedia.org/..." class="w-2/3 px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                  <input id="adm-lic" type="text" placeholder="CC BY-SA 4.0" class="w-1/3 px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                </div>
              </div>
              <div class="col-span-2">
                <label class="block text-slate-400 mb-1">수정 사유 / 출처 메모</label>
                <input id="adm-note" type="text" value="공식 축구협회 기록 대조 후 관리자 반영" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
              </div>
            </div>
            <button onclick="window.app.submitAdminPlayer()" class="w-full py-2.5 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs">
              저장 및 감사 로그 기록
            </button>
          </div>

          <!-- Merge Duplicate Players & CSV Import -->
          <div class="space-y-5">
            <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
              <h3 class="text-base font-black text-sky-400">2. 중복 선수 병합 (Merge Duplicates)</h3>
              <div class="grid grid-cols-2 gap-2.5 text-xs">
                <div>
                  <label class="block text-slate-400 mb-1">유지할 기준 선수 ID (Keep)</label>
                  <input id="adm-merge-keep" type="number" placeholder="예: 101" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                </div>
                <div>
                  <label class="block text-slate-400 mb-1">통합 후 삭제할 선수 ID (Remove)</label>
                  <input id="adm-merge-rem" type="number" placeholder="예: 205" class="w-full px-2.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white" />
                </div>
              </div>
              <button onclick="window.app.submitAdminMerge()" class="px-4 py-2 rounded-xl bg-sky-400 hover:bg-sky-300 text-slate-950 font-black text-xs">
                중복 선수 병합 실행
              </button>
            </div>

            <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
              <h3 class="text-base font-black text-emerald-400">3. CSV 선수 데이터 일괄 가져오기</h3>
              <p class="text-xs text-slate-400">필수 헤더: <code>country_fifa_code,name_ko,name_en,primary_position,official_caps,official_goals,career_start_year,career_end_year</code></p>
              <input id="adm-csv-file" type="file" accept=".csv" class="block w-full text-xs text-slate-300" />
              <button onclick="window.app.submitAdminCsv()" class="px-4 py-2 rounded-xl bg-emerald-400 hover:bg-emerald-300 text-slate-950 font-black text-xs">
                CSV 파일 업로드 및 적재
              </button>
            </div>
          </div>
        </div>

        <!-- Audit Logs Table -->
        <div class="rounded-2xl bg-slate-900/95 border border-slate-800 p-5 space-y-3">
          <h3 class="text-base font-black text-white">관리자 데이터 수정 이력 (Audit Trail)</h3>
          <div class="space-y-2 text-xs max-h-72 overflow-y-auto custom-scrollbar">
            ${state.adminLogs.length === 0 ? `<div class="text-slate-500">아직 기록된 수정 이력이 없습니다.</div>` : state.adminLogs.map(l => `
              <div class="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between gap-2">
                <div>
                  <span class="px-2 py-0.5 rounded bg-amber-400/20 text-amber-300 font-bold">${escapeHtml(l.action_type)}</span>
                  <span class="text-white font-semibold ml-2">${escapeHtml(l.admin_note || '')}</span>
                  <span class="text-slate-400 ml-2">(대상: ${escapeHtml(l.target_table)} #${escapeHtml(l.target_id)})</span>
                </div>
                <span class="text-slate-500">${escapeHtml(l.created_at)}</span>
              </div>
            `).join('')}
          </div>
        </div>
      </div>
    `;
  }

  // ============================================================================
  // MODALS: PLAYER PROFILE DETAIL & AI API KEY CONFIGURATION
  // ============================================================================
  async function openPlayerModal(playerId) {
    if (!playerId) return;
    try {
      const resp = await fetch(`/api/players/${playerId}`);
      if (!resp.ok) throw new Error('선수 정보를 불러오지 못했습니다.');
      const p = await resp.json();
      const nc = (p.national_team_careers && p.national_team_careers[0]) || {};
      const cObj = state.countries.find(c => c.fifa_code === p.nationality_code) || {};

      const modalRoot = document.getElementById('modal-root');
      modalRoot.innerHTML = `
        <div class="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4" onclick="window.app.closeModal()">
          <div class="bg-slate-900 border border-slate-700 rounded-3xl max-w-2xl w-full p-6 space-y-5 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar" onclick="event.stopPropagation()">
            <div class="flex items-start justify-between gap-4 border-b border-slate-800 pb-4">
              <div class="flex items-center gap-4">
                ${renderPlayerAvatarHtml(p, cObj, 'w-20 h-20', 'text-xl')}
                <div>
                  <div class="flex items-center gap-2 flex-wrap">
                    <span class="text-lg">${escapeHtml(nc.flag_emoji || cObj.flag_emoji || '')}</span>
                    <span class="text-xs font-bold text-amber-400">${escapeHtml(nc.country_name_ko || p.nationality_code)} 국가대표</span>
                    <span class="px-2 py-0.5 rounded bg-slate-800 text-xs font-black text-white">${escapeHtml(p.primary_position)}</span>
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold ${p.is_active_player ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'}">
                      ${p.is_active_player ? '현역' : '은퇴'}
                    </span>
                  </div>
                  <h2 class="text-xl sm:text-2xl font-black text-white mt-1">${escapeHtml(formatNameKoEn(p))}</h2>
                  ${p.name_native && p.name_native !== p.name_en ? `<div class="text-xs text-slate-400">원어 표기: ${escapeHtml(p.name_native)}</div>` : ''}
                </div>
              </div>
              <button onclick="window.app.closeModal()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold">✕</button>
            </div>

            <!-- Objective Facts Section (Section 8: 객관적인 사실 중심) -->
            <div class="space-y-3">
              <h3 class="text-xs font-black uppercase tracking-wider text-emerald-400">📊 출처 기반 객관적 기록 (Verified Historical Facts)</h3>
              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div class="text-slate-400">공식 A매치 출전</div>
                  <div class="text-lg font-black text-white mt-0.5">${nc.official_caps || '-'}경기</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div class="text-slate-400">공식 A매치 득점</div>
                  <div class="text-lg font-black text-emerald-400 mt-0.5">${nc.official_goals ?? '-'}골</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div class="text-slate-400">대표팀 활동 기간</div>
                  <div class="text-sm font-black text-amber-300 mt-1">${escapeHtml(nc.active_period_label || '-')}</div>
                </div>
                <div class="p-3 rounded-xl bg-slate-950 border border-slate-800">
                  <div class="text-slate-400">생년월일 / 신체</div>
                  <div class="text-xs font-bold text-slate-200 mt-1">
                    ${escapeHtml(p.date_of_birth || (p.birth_year ? p.birth_year + '년생' : '미상'))}
                    ${p.height_cm ? ` · ${p.height_cm}cm` : ''}
                    ${p.preferred_foot ? ` · ${p.preferred_foot}` : ''}
                  </div>
                </div>
              </div>

              <!-- Multi-country careers if any -->
              ${(p.national_team_careers || []).length > 1 ? `
                <div class="p-3 rounded-xl bg-amber-400/10 border border-amber-400/30 text-xs space-y-1">
                  <div class="font-bold text-amber-300">🌐 복수 국가대표팀 경력 분리 기록 (국가별 합산 금지 원칙 적용):</div>
                  ${p.national_team_careers.map(c => `
                    <div>• ${escapeHtml(c.country_name_ko)} (${escapeHtml(c.represented_fifa_code)}): ${c.official_caps}경기 ${c.official_goals}골 (${escapeHtml(c.active_period_label)}) — ${c.is_eligible_30_caps ? '30회 이상 적격' : '30회 미만 제외'}</div>
                  `).join('')}
                </div>
              ` : ''}

              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 text-xs">
                <div><strong>🏟️ 주요 소속 클럽:</strong> ${escapeHtml(p.major_clubs_ko || '공식 대표팀 기록 아카이브 등재 선수')}</div>
                <div><strong>🏆 주요 우승 및 수상 기록:</strong> ${escapeHtml(p.major_honors_ko || p.individual_awards_ko || '국가대표 A매치 30회 이상 공식 출전')}</div>
                ${p.world_cup_participations ? `<div><strong>🌍 월드컵 참가 이력:</strong> ${escapeHtml(p.world_cup_participations)}</div>` : ''}
                ${nc.discrepancy_note_ko ? `<div class="text-amber-300"><strong>ℹ️ 출처 간 기록 비교 주석:</strong> ${escapeHtml(nc.discrepancy_note_ko)}</div>` : ''}
              </div>
            </div>

            <!-- Tactical & Play Style Summary (Separated from objective facts per Section 8) -->
            <div class="space-y-2">
              <h3 class="text-xs font-black uppercase tracking-wider text-sky-400">🧠 전술 프로필 및 플레이 스타일 요약 (Tactical Profile)</h3>
              <div class="p-3.5 rounded-xl bg-slate-950 border border-slate-800 space-y-1.5 text-xs leading-relaxed">
                <div><strong>주요 역할:</strong> ${escapeHtml(p.primary_role_ko || p.primary_position)}</div>
                <div><strong>플레이 스타일:</strong> ${escapeHtml(p.play_style_ko || '')}</div>
                ${p.attack_defense_traits_ko ? `<div><strong>공수 특성:</strong> ${escapeHtml(p.attack_defense_traits_ko)}</div>` : ''}
                ${p.tactical_fit_role_ko ? `<div><strong>추천 전술 배치:</strong> ${escapeHtml(p.tactical_fit_role_ko)}</div>` : ''}
              </div>
            </div>

            <!-- Data Sources & Image License Attribution -->
            <div class="pt-3 border-t border-slate-800 text-[11px] text-slate-400 space-y-1">
              <div><strong>데이터 출처:</strong> ${escapeHtml(nc.record_source_name || 'RSSSF / Wikipedia / Transfermarkt')} (확인일: ${escapeHtml(nc.verified_date || '2026-10-07')})</div>
              ${p.original_source_name ? `<div><strong>이미지 출처 및 라이선스:</strong> ${escapeHtml(p.original_source_name)} (${escapeHtml(p.license_info || '')})</div>` : `<div><strong>이미지 안내:</strong> 외부 초상권 보호를 위해 국가별 컬러 유니폼 아바타로 표시됩니다.</div>`}
            </div>
          </div>
        </div>
      `;
    } catch (e) {
      showToast(e.message, 'error');
    }
  }

  function closeModal() {
    const modalRoot = document.getElementById('modal-root');
    if (modalRoot) modalRoot.innerHTML = '';
  }

  // ============================================================================
  // CORE CONTROLLER LOGIC & STATE ACTIONS
  // ============================================================================
  function render() {
    updateNavHighlight();
    updateAiBadge();
    const root = document.getElementById('app-root');
    if (!root) return;
    if (state.view === 'home') root.innerHTML = renderHomeView();
    else if (state.view === 'builder') root.innerHTML = renderBuilderView();
    else if (state.view === 'board') root.innerHTML = renderBoardView();
    else if (state.view === 'arena') root.innerHTML = renderArenaView();
    else if (state.view === 'database') root.innerHTML = renderDatabaseView();
    else if (state.view === 'quality') root.innerHTML = renderQualityView();
    else if (state.view === 'admin') root.innerHTML = renderAdminView();
  }

  function initBuilderSlotsForFormation(formationCode, preserveExistingPlayers = true) {
    const list = (state.formations && state.formations.length) ? state.formations : DEFAULT_FORMATIONS;
    const fm = list.find(f => f.code === formationCode) || list[0];
    if (!fm) return;
    state.builderFormationCode = fm.code;

    const rawSlots = Array.isArray(fm.slots) ? fm.slots : (typeof fm.slots === 'string' ? JSON.parse(fm.slots) : (fm.slots_json ? JSON.parse(fm.slots_json) : []));

    if (!preserveExistingPlayers || !state.builderSlots.length) {
      state.builderSlots = rawSlots.map((sdef, idx) => ({
        slot_index: idx,
        slot_code: sdef.slot_code,
        label_ko: sdef.label_ko,
        group: sdef.group,
        x: sdef.x,
        y: sdef.y,
        compatible: sdef.compatible || [],
        player: null,
        is_captain: false,
        suitability: null
      }));
      return;
    }

    // Preserve existing placed players by matching positions and position groups
    const existingPlayers = state.builderSlots.map(s => s.player).filter(Boolean);
    const usedIds = new Set();
    const newSlots = rawSlots.map((sdef, idx) => ({
      slot_index: idx,
      slot_code: sdef.slot_code,
      label_ko: sdef.label_ko,
      group: sdef.group,
      x: sdef.x,
      y: sdef.y,
      compatible: sdef.compatible || [],
      player: null,
      is_captain: false,
      suitability: null
    }));

    // 1st pass: exact slot_code match (e.g. GK -> GK, LB -> LB, ST -> ST)
    newSlots.forEach(ns => {
      const match = existingPlayers.find(p => !usedIds.has(p.id || p.player_id) && p.primary_position === ns.slot_code);
      if (match) {
        usedIds.add(match.id || match.player_id);
        ns.player = match;
      }
    });

    // 2nd pass: position group match (DF -> DF, MF -> MF, FW -> FW)
    newSlots.forEach(ns => {
      if (!ns.player) {
        const match = existingPlayers.find(p => !usedIds.has(p.id || p.player_id) && p.position_group === ns.group);
        if (match) {
          usedIds.add(match.id || match.player_id);
          ns.player = match;
        }
      }
    });

    // 3rd pass: any remaining unused outfield players
    newSlots.forEach(ns => {
      if (!ns.player && ns.group !== 'GK') {
        const match = existingPlayers.find(p => !usedIds.has(p.id || p.player_id) && p.primary_position !== 'GK');
        if (match) {
          usedIds.add(match.id || match.player_id);
          ns.player = match;
        }
      }
    });

    // Recompute suitability and captaincy
    newSlots.forEach(ns => {
      if (ns.player) {
        ns.suitability = computeClientSuitability(ns.player, ns);
        ns.is_captain = Boolean(state.builderCaptainId && (ns.player.id || ns.player.player_id) === state.builderCaptainId);
      }
    });

    state.builderSlots = newSlots;
  }

  async function loadCountryPlayersForBuilder(fifaCode) {
    const resp = await fetch(`/api/players?country_code=${encodeURIComponent(fifaCode)}&eligible_only=true&limit=600`);
    const data = await resp.json();
    state.builderCountryPlayers = data.players || [];
  }

  function autoFillBuilderLegendXI() {
    const pool = state.builderCountryPlayers || [];
    if (!pool.length) return;
    const used = new Set();

    state.builderSlots.forEach((slot) => {
      // Find best unused player who fits this slot naturally or secondarily
      let best = null;
      let bestScore = -1;
      for (const p of pool) {
        if (used.has(p.id)) continue;
        if (slot.slot_code === 'GK' && p.primary_position !== 'GK') continue;
        if (slot.slot_code !== 'GK' && p.primary_position === 'GK') continue;
        const suit = computeClientSuitability(p, slot);
        const legendBonus = p.is_legend_test_case ? 45 : 0;
        const totalScore = suit.score * 2 + legendBonus + Math.min(180, p.official_caps);
        if (totalScore > bestScore) {
          bestScore = totalScore;
          best = p;
        }
      }
      if (best) {
        used.add(best.id);
        slot.player = best;
        slot.suitability = computeClientSuitability(best, slot);
      }
    });

    // Set captain to highest cap player in the XI
    let topCapP = null;
    state.builderSlots.forEach(s => {
      if (s.player && (!topCapP || s.player.official_caps > topCapP.official_caps)) {
        topCapP = s.player;
      }
    });
    if (topCapP) {
      state.builderCaptainId = topCapP.id;
      state.builderSlots.forEach(s => {
        s.is_captain = Boolean(s.player && s.player.id === topCapP.id);
      });
    }
    state.lastSavedLineupResult = null;
    render();
    showToast('역대 레전드 및 최다 출전 기준으로 11명이 자동 배치되었습니다.', 'success');
  }

  async function startCountryBuilder(fifaCode) {
    state.builderCountryCode = fifaCode;
    const cObj = getBuilderCountryObj();
    state.builderTeamName = `${cObj.name_ko || fifaCode} 역대 최강 XI`;
    state.builderDescription = `1950년대~2020년대 시대를 초월한 ${cObj.name_ko || fifaCode} 국가대표 올타임 드림팀`;
    state.lastSavedLineupResult = null;
    state.swapSourceSlotIndex = null;
    await loadCountryPlayersForBuilder(fifaCode);
    initBuilderSlotsForFormation(state.builderFormationCode, false);
    autoFillBuilderLegendXI();
    state.view = 'builder';
    render();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  function buildLineupPayload() {
    const filled = state.builderSlots.filter(s => s.player);
    if (filled.length !== 11) {
      showToast(`11명을 모두 배치해야 합니다. (현재 ${filled.length}/11명 배치됨)`, 'warn');
      return null;
    }
    return {
      country_fifa_code: state.builderCountryCode,
      team_name: state.builderTeamName || '역대 최강 XI',
      formation_code: state.builderFormationCode,
      tactical_style: state.builderTacticalStyle,
      board_color_theme: state.builderBoardTheme,
      team_description: state.builderDescription,
      captain_player_id: state.builderCaptainId,
      players: state.builderSlots.map((s, idx) => ({
        slot_index: idx,
        slot_code: s.slot_code,
        slot_label_ko: s.label_ko,
        player_id: s.player.id || s.player.player_id,
        x: s.x,
        y: s.y,
        jersey_number: s.player.jersey_number || s.player.fallback_number || (idx + 1),
        is_captain: Boolean(state.builderCaptainId && (s.player.id || s.player.player_id) === state.builderCaptainId)
      }))
    };
  }

  async function saveCurrentLineup(silent = false) {
    const payload = buildLineupPayload();
    if (!payload) return null;
    try {
      const resp = await fetch('/api/lineups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.detail || '팀 저장 실패');
      state.lastSavedLineupResult = data;
      // Refresh savedLineups list
      const listResp = await fetch('/api/lineups');
      const listData = await listResp.json();
      state.savedLineups = listData.lineups || [];
      if (!silent) {
        render();
        showToast('베스트11이 저장되었으며 고유 공유 URL이 생성되었습니다!', 'success');
      }
      return data;
    } catch (e) {
      showToast(e.message, 'error');
      return null;
    }
  }

  
  // ============================================================================
  // VISITOR COUNTER & KAKAO IMAGE SHARE SYSTEM
  // ============================================================================
    // ============================================================================
  // PURE UNIQUE VISITOR (UV) TRACKING SYSTEM
  // ============================================================================
  function trackDailyUniqueVisit() {
    try {
      const today = new Date().toISOString().slice(0, 10);
      const lastRecorded = localStorage.getItem('all_time_xi_last_unique_visit');
      if (lastRecorded === today) {
        // Already recorded today on this device -> do not increment
        return;
      }
      // Record today's unique visit once
      localStorage.setItem('all_time_xi_last_unique_visit', today);
      fetch('/api/stats/visit', { method: 'POST' })
        .then(r => r.json())
        .then(stats => {
          if (stats) updateVisitorCounterUI(stats);
        })
        .catch(() => {});
    } catch (e) {}
  }

  function updateVisitorCounterUI(stats) {
    try {
      try {
        localStorage.removeItem('all_time_xi_v_stats');
      } catch (e) {}

      if (!stats) return;
      let today = stats.today_visitors !== undefined ? Number(stats.today_visitors) : null;
      let total = stats.total_visitors !== undefined ? Number(stats.total_visitors) : null;
      if (today !== null && total !== null && total < today) {
        total = today;
      }

      const elToday = document.getElementById('visitor-today-count');
      const elTotal = document.getElementById('visitor-total-count');
      if (elToday && today !== null) elToday.textContent = Number(today).toLocaleString();
      if (elTotal && total !== null) elTotal.textContent = Number(total).toLocaleString();
    } catch (e) {
      console.warn('visitor counter ui error:', e);
    }
  }

  let lastCapturedBlob = null;
  let lastCapturedDataUrl = null;
  let lastCapturedTitle = '';

  async function ensureLineupSaved() {
    if (state.lastSavedLineupResult && state.lastSavedLineupResult.share_slug) {
      return state.lastSavedLineupResult.share_slug;
    }
    const payload = buildLineupPayload();
    if (!payload) return null;
    try {
      const resp = await fetch('/api/lineups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (resp.ok) {
        const data = await resp.json();
        state.lastSavedLineupResult = data;
        return data.share_slug;
      }
    } catch (e) {
      console.warn('Auto-save for image capture error:', e);
    }
    return null;
  }

  async function preparePitchBoardForCapture(pitchEl) {
    if (!pitchEl) return;
    const imgs = Array.from(pitchEl.querySelectorAll('img'));
    await Promise.all(imgs.map(async (img) => {
      const src = img.getAttribute('src');
      if (!src || src.startsWith('data:')) return;
      try {
        const proxyUrl = `/api/proxy-image?url=${encodeURIComponent(src)}`;
        const resp = await fetch(proxyUrl);
        if (resp.ok) {
          const blob = await resp.blob();
          const base64 = await new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
          });
          img.setAttribute('src', base64);
        }
      } catch (err) {
        console.warn('preparePitchBoardForCapture image convert error:', err);
      }
    }));
  }

  async function capturePitchAsBlob() {
    // 1. WYSIWYG Client-side Screen Capture of exact pitch board
    const pitchEl = document.getElementById('tactical-pitch-board');
    if (window.html2canvas && pitchEl) {
      try {
        // Pre-convert images to base64 Data URLs so canvas is never tainted
        await preparePitchBoardForCapture(pitchEl);

        const canvas = await window.html2canvas(pitchEl, {
          scale: 2.5,
          useCORS: true,
          allowTaint: false,
          backgroundColor: '#070b14',
          logging: false
        });
        const dataUrl = canvas.toDataURL('image/png');
        const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/png'));
        if (blob) {
          lastCapturedBlob = blob;
          lastCapturedDataUrl = dataUrl;
          return { blob, dataUrl };
        }
      } catch (err) {
        console.warn('html2canvas client capture error, falling back to server PNG:', err);
      }
    }

    // 2. Guaranteed server PNG generation:
    // Auto-save lineup if not yet saved to obtain a real share slug
    const slug = await ensureLineupSaved();
    if (slug) {
      try {
        const sResp = await fetch(`/api/lineups/${slug}/png?layout=portrait`);
        if (sResp.ok) {
          const sBlob = await sResp.blob();
          const sDataUrl = URL.createObjectURL(sBlob);
          lastCapturedBlob = sBlob;
          lastCapturedDataUrl = sDataUrl;
          return { blob: sBlob, dataUrl: sDataUrl };
        }
      } catch (e) {
        console.warn('Server PNG fetch fallback error:', e);
      }
    }

    return { blob: null, dataUrl: null };
  }

  async function shareLineupImageDirectly() {
    const filled = state.builderSlots.filter(s => s.player).length;
    if (filled < 11) {
      const proceed = confirm(`현재 11명 중 ${filled}명만 배치되어 있습니다.\n이 상태로 전술판 이미지를 카카오톡으로 공유하시겠습니까?`);
      if (!proceed) return;
    }

    showToast('전술판 고해상도 이미지를 준비하고 있습니다...', 'info');

    const countryObj = getCountryByCode(state.builderCountryCode) || {};
    const teamTitle = state.builderTeamName || `${countryObj.name_ko || state.builderCountryCode} 역대 올타임 베스트11`;
    lastCapturedTitle = teamTitle;

    const { blob, dataUrl } = await capturePitchAsBlob();
    if (!blob) {
      showToast('이미지 캡처에 실패하여 링크 공유로 대체합니다.', 'warning');
      return shareLineupDirectly();
    }

    const fileName = `ALL-TIME-XI-${state.builderCountryCode || 'TEAM'}.png`;
    const imageFile = new File([blob], fileName, { type: 'image/png' });

    // 1. Mobile Web Share API Level 2 (Directly shares actual image photo to KakaoTalk)
    if (navigator.canShare && navigator.canShare({ files: [imageFile] })) {
      try {
        await navigator.share({
          files: [imageFile],
          title: `[ALL-TIME XI] ${teamTitle}`,
          text: `${teamTitle} 전술판 이미지입니다! https://all-time-xi.vercel.app/`
        });
        showToast('카카오톡 사진 공유 창이 열렸습니다!', 'success');
        return;
      } catch (err) {
        if (err.name === 'AbortError') return;
        console.warn('navigator.share files error:', err);
      }
    }

    // 2. Desktop: Copy image directly to Clipboard (Ctrl+V into PC KakaoTalk)
    let copiedToClipboard = false;
    if (navigator.clipboard && window.ClipboardItem) {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        copiedToClipboard = true;
      } catch (e) {
        console.warn('Clipboard image write not permitted:', e);
      }
    }

    // Download image file as companion fallback
    try {
      const a = document.createElement('a');
      a.href = dataUrl;
      a.download = fileName;
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) {}

    // Show interactive modal
    showImageShareModal(dataUrl, blob, teamTitle, copiedToClipboard);
  }

  function showImageShareModal(dataUrl, blob, teamTitle, copiedToClipboard, slug = '') {
    const modalRoot = document.getElementById('modal-root');
    if (!modalRoot) return;

    const countryObj = getCountryByCode(state.builderCountryCode) || {};
    const teamName = teamTitle || `${countryObj.name_ko || ''} 역대 베스트11`;
    const fullPngUrl = dataUrl.startsWith('http') || dataUrl.startsWith('/') || dataUrl.startsWith('data:') 
      ? dataUrl 
      : `${window.location.origin}${dataUrl}`;

    modalRoot.innerHTML = `
      <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/90 backdrop-blur-md animate-fade-in" onclick="if(event.target === this) window.app.closeModal()">
        <div class="relative w-full max-w-2xl bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl p-5 sm:p-6 overflow-hidden max-h-[95vh] flex flex-col">
          <!-- Header -->
          <div class="flex items-center justify-between pb-3.5 border-b border-slate-800">
            <div class="flex items-center gap-2.5">
              <span class="text-2xl">🖼️</span>
              <div>
                <h3 class="text-base sm:text-lg font-black text-slate-100 flex items-center gap-2">
                  <span>${escapeHtml(teamName)}</span>
                  <span class="text-xs px-2 py-0.5 rounded-full bg-amber-400/20 text-amber-300 font-bold border border-amber-400/30">완성 이미지</span>
                </h3>
                <p class="text-xs text-slate-400 mt-0.5">고해상도 완성 전술판 미리보기 및 카카오톡 전송</p>
              </div>
            </div>
            <button onclick="window.app.closeModal()" class="text-slate-400 hover:text-white text-2xl font-bold p-1 leading-none">✕</button>
          </div>

          <!-- PC 카카오톡 친절 3단계 안내 가이드 카드 -->
          <div class="mt-3.5 p-4 sm:p-4.5 rounded-2xl bg-gradient-to-br from-yellow-500/20 via-amber-500/10 to-slate-900 border-2 border-yellow-400/50 shadow-xl space-y-3">
            <div class="flex flex-wrap items-center justify-between gap-2">
              <div class="flex items-center gap-2">
                <span class="text-2xl">💬</span>
                <span class="text-sm sm:text-base font-black text-yellow-300 tracking-tight">PC 카카오톡으로 이미지 바로 전송하는 법</span>
              </div>
              <div class="flex items-center gap-1.5 flex-wrap">
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-emerald-500/20 border border-emerald-400/40 text-emerald-300 text-xs font-bold">
                  <span>✓</span> 클립보드 복사됨
                </span>
                <span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-blue-500/20 border border-blue-400/40 text-blue-300 text-xs font-bold">
                  <span>💾</span> PNG 다운로드됨
                </span>
              </div>
            </div>

            <!-- 3-Step Walkthrough Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 pt-0.5">
              <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 flex items-start gap-2.5">
                <span class="w-6 h-6 rounded-full bg-yellow-400 text-slate-950 font-black text-xs flex items-center justify-center shrink-0 mt-0.5 shadow">1</span>
                <div>
                  <div class="text-xs font-bold text-slate-200">카톡 대화창 클릭</div>
                  <div class="text-[11px] text-slate-400 mt-0.5 leading-snug">PC 카톡 친구 또는 단톡방 대화 입력창을 클릭하세요.</div>
                </div>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-950/80 border border-yellow-400/40 flex items-start gap-2.5 ring-1 ring-yellow-400/20">
                <span class="w-6 h-6 rounded-full bg-yellow-400 text-slate-950 font-black text-xs flex items-center justify-center shrink-0 mt-0.5 shadow">2</span>
                <div>
                  <div class="text-xs font-black text-yellow-300 flex items-center gap-1">
                    <span class="px-1.5 py-0.5 rounded bg-yellow-400 text-slate-950 font-mono text-[10px] font-bold">Ctrl + V</span>
                    <span>붙여넣기</span>
                  </div>
                  <div class="text-[11px] text-slate-300 mt-0.5 leading-snug">대화창에서 <strong>Ctrl + V</strong>를 누르면 이미지 첨부창이 뜹니다.</div>
                </div>
              </div>
              <div class="p-2.5 rounded-xl bg-slate-950/80 border border-slate-800 flex items-start gap-2.5">
                <span class="w-6 h-6 rounded-full bg-emerald-400 text-slate-950 font-black text-xs flex items-center justify-center shrink-0 mt-0.5 shadow">3</span>
                <div>
                  <div class="text-xs font-bold text-emerald-300">엔터(Enter) 전송</div>
                  <div class="text-[11px] text-slate-400 mt-0.5 leading-snug">고화질 전술판 완성 이미지가 채팅방에 즉시 전송됩니다!</div>
                </div>
              </div>
            </div>

            <!-- 백업 안내: 자동 다운로드 및 파일 첨부 -->
            <div class="pt-2 border-t border-yellow-400/20 text-xs text-slate-300 flex items-start sm:items-center gap-2 leading-relaxed">
              <span class="text-base shrink-0">💡</span>
              <div>
                <strong>붙여넣기가 안 될 때 백업 방법:</strong> 방금 PC 다운로드 폴더로 자동 저장된 <span class="text-yellow-300 font-mono font-bold">PNG 파일</span>을 마우스로 카카오톡 대화창에 <strong>쓱 끌어다 놓기(드래그)</strong> 하셔도 바로 전송됩니다.
              </div>
            </div>
          </div>

          <!-- Large High-Res Image Preview Box -->
          <div class="my-3.5 rounded-xl border border-slate-800 bg-slate-950 p-2 overflow-auto flex-1 flex items-center justify-center max-h-[58vh] group relative cursor-zoom-in" onclick="window.open('${fullPngUrl}', '_blank')" title="클릭하면 새 탭에서 고화질 원본으로 열립니다">
            <img src="${fullPngUrl}" alt="전술판 고해상도 완성 이미지" class="max-h-[54vh] w-auto object-contain rounded-lg shadow-2xl transition group-hover:scale-[1.01]" />
            <div class="absolute bottom-3 right-3 px-2.5 py-1 rounded-md bg-slate-900/80 backdrop-blur-sm border border-slate-700 text-[11px] text-slate-300 font-bold opacity-0 group-hover:opacity-100 transition pointer-events-none">
              🔍 클릭하여 새 탭에서 크게 보기
            </div>
          </div>

          <!-- Action Footer Buttons -->
          <div class="pt-3 border-t border-slate-800 flex flex-wrap items-center justify-between gap-2.5">
            <div class="flex items-center gap-2">
              <button onclick="window.open('${fullPngUrl}', '_blank')" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold border border-slate-700 transition flex items-center gap-1.5">
                <span>🖼️ 새 탭에서 열기</span>
              </button>
              <button onclick="window.app.copyImageToClipboard()" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold border border-slate-700 transition flex items-center gap-1.5">
                <span>📋 이미지 복사</span>
              </button>
              <a href="${fullPngUrl}" download="ALL-TIME-XI-${teamName}.png" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold border border-slate-700 transition flex items-center gap-1.5">
                <span>💾 PNG 다운로드</span>
              </a>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="window.app.copyImageToClipboard()" class="px-4 py-2 rounded-xl bg-yellow-400 hover:bg-yellow-300 text-slate-950 text-xs sm:text-sm font-black shadow-lg shadow-yellow-400/20 transition flex items-center gap-1.5">
                <span>📋 이미지 복사 (카톡에 Ctrl+V)</span>
              </button>
              <button onclick="window.app.closeModal()" class="px-3 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-400 text-xs sm:text-sm font-semibold border border-slate-800">
                닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function openSavedLineupImagePreview(teamTitle, slug) {
    const pngUrl = `/api/lineups/${slug}/png?layout=portrait`;
    lastCapturedBlob = null;
    lastCapturedDataUrl = pngUrl;
    lastCapturedTitle = teamTitle;
    showImageShareModal(pngUrl, null, teamTitle, false, slug);
  }

  async function openLineupImagePreview() {
    const filled = state.builderSlots.filter(s => s.player).length;
    if (filled < 11) {
      const proceed = confirm(`현재 11명 중 ${filled}명만 배치되어 있습니다.\n이 상태로 전술판 이미지를 카카오톡으로 공유하시겠습니까?`);
      if (!proceed) return;
    }

    showToast('전술판 고해상도 완성 이미지를 준비하고 있습니다...', 'info');

    const countryObj = getCountryByCode(state.builderCountryCode) || {};
    const teamTitle = state.builderTeamName || `${countryObj.name_ko || state.builderCountryCode} 역대 올타임 베스트11`;
    lastCapturedTitle = teamTitle;

    const { blob, dataUrl } = await capturePitchAsBlob();
    if (!blob || !dataUrl) {
      showToast('이미지 생성에 실패했습니다. 선수를 배치한 후 다시 시도해주세요.', 'error');
      return;
    }

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    const fileName = `ALL-TIME-XI-${state.builderCountryCode || 'TEAM'}.png`;
    const imageFile = new File([blob], fileName, { type: 'image/png' });

    // 1. Mobile: Native Web Share API with real image file directly to KakaoTalk
    if (isMobile && navigator.canShare && navigator.canShare({ files: [imageFile] })) {
      try {
        await navigator.share({
          files: [imageFile],
          title: `[ALL-TIME XI] ${teamTitle}`,
          text: `${teamTitle} 전술판 완성 이미지입니다! https://all-time-xi.vercel.app/`
        });
        showToast('카카오톡 사진 공유 창이 열렸습니다!', 'success');
        return;
      } catch (err) {
        if (err.name === 'AbortError') return;
      }
    }

    // 2. Desktop PC: Copy image directly to Clipboard and auto download as companion
    let copied = false;
    if (navigator.clipboard && window.ClipboardItem) {
      try {
        await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
        copied = true;
        showToast('✅ 이미지가 복사되고 PNG 파일이 다운로드되었습니다! 카톡 대화창에서 Ctrl + V 하세요.', 'success');
      } catch (e) {
        console.warn('Clipboard write error:', e);
      }
    }

    // Auto download companion PNG file on PC
    try {
      const dlLink = document.createElement('a');
      dlLink.href = dataUrl;
      dlLink.download = fileName;
      document.body.appendChild(dlLink);
      dlLink.click();
      document.body.removeChild(dlLink);
    } catch (e) {
      console.warn('Auto download error:', e);
    }

    const slug = (state.lastSavedLineupResult && state.lastSavedLineupResult.share_slug) || '';
    showImageShareModal(dataUrl, blob, teamTitle, copied, slug);
  }

  function launchPcKakaoTalk() {
    try {
      window.location.href = 'kakaotalk://';
      showToast('카카오톡 PC버전을 실행합니다. 대화창에 Ctrl + V (붙여넣기) 하세요!', 'success');
    } catch (e) {
      showToast('카카오톡 대화창에서 Ctrl + V (붙여넣기)를 눌러주세요!', 'info');
    }
  }

  async function copyImageToClipboard() {
    if (!lastCapturedBlob && lastCapturedDataUrl) {
      try {
        const resp = await fetch(lastCapturedDataUrl);
        if (resp.ok) {
          lastCapturedBlob = await resp.blob();
        }
      } catch (e) {
        console.warn('Failed to fetch blob from dataUrl', e);
      }
    }
    if (!lastCapturedBlob) {
      if (lastCapturedDataUrl) {
        window.open(lastCapturedDataUrl, '_blank');
        showToast('새 탭에서 이미지가 열렸습니다. 우클릭하여 [이미지 복사] 하세요!', 'info');
      } else {
        showToast('복사할 이미지를 찾을 수 없습니다.', 'warning');
      }
      return;
    }
    try {
      if (navigator.clipboard && window.ClipboardItem) {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': lastCapturedBlob })
        ]);
        showToast('전술판 이미지가 클립보드에 복사되었습니다! 카톡 대화창에서 Ctrl+V 하세요.', 'success');
      } else {
        showToast('이미지 파일로 다운로드되었습니다. 카톡 창에 드래그하거나 첨부하세요.', 'info');
      }
    } catch (e) {
      showToast('카톡 대화창에서 Ctrl+V를 누르거나 다운로드된 이미지를 사용해주세요.', 'info');
    }
  }

  async function shareImageViaNativeShare() {
    if (!lastCapturedBlob) return;
    const fileName = `ALL-TIME-XI-${state.builderCountryCode || 'TEAM'}.png`;
    const imageFile = new File([lastCapturedBlob], fileName, { type: 'image/png' });
    if (navigator.canShare && navigator.canShare({ files: [imageFile] })) {
      try {
        await navigator.share({
          files: [imageFile],
          title: `[ALL-TIME XI] ${lastCapturedTitle}`,
          text: `${lastCapturedTitle} 전술판 이미지입니다! https://all-time-xi.vercel.app/`
        });
        showToast('카카오톡 사진 공유가 실행되었습니다!', 'success');
        closeModal();
      } catch (e) {
        if (e.name !== 'AbortError') showToast(e.message, 'error');
      }
    } else {
      copyImageToClipboard();
      launchPcKakaoTalk();
    }
  }

  async function shareSavedLineupDirectly(teamTitle, slug) {
    showToast('카카오톡 전술판 완성 이미지를 준비하고 있습니다...', 'info');
    const shareUrl = `${window.location.origin}/team/${slug}`;
    const pngUrl = `${window.location.origin}/api/lineups/${slug}/png?layout=portrait`;

    let blob = null;
    try {
      const resp = await fetch(pngUrl);
      if (resp.ok) {
        blob = await resp.blob();
        lastCapturedBlob = blob;
        lastCapturedDataUrl = pngUrl;
      }
    } catch (e) {
      console.warn('Failed to fetch lineup PNG for share', e);
    }

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);

    // 1. Mobile: Native Web Share API with real image file directly to KakaoTalk!
    if (isMobile && blob) {
      const fileName = `${slug}.png`;
      const file = new File([blob], fileName, { type: 'image/png' });
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        try {
          await navigator.share({
            files: [file],
            title: `[ALL-TIME XI] ${teamTitle}`,
            text: `${teamTitle} 전술판 완성 이미지입니다! ${shareUrl}`
          });
          showToast('카카오톡 사진 공유 창이 열렸습니다!', 'success');
          return;
        } catch (e) {
          if (e.name === 'AbortError') return;
        }
      }
    }

    // 2. Desktop PC: Copy image directly to clipboard for instant Ctrl+V into KakaoTalk!
    let copied = false;
    if (blob && navigator.clipboard && window.ClipboardItem) {
      try {
        await navigator.clipboard.write([
          new ClipboardItem({ 'image/png': blob })
        ]);
        copied = true;
        showToast('✅ 이미지가 복사되고 PNG 파일이 다운로드되었습니다! 카톡 대화창에서 Ctrl + V 하세요.', 'success');
      } catch (e) {}
    }

    // Auto download companion PNG file on PC
    try {
      const dlLink = document.createElement('a');
      dlLink.href = pngUrl;
      dlLink.download = `ALL-TIME-XI-${teamTitle}.png`;
      document.body.appendChild(dlLink);
      dlLink.click();
      document.body.removeChild(dlLink);
    } catch (e) {}

    // Also copy URL to clipboard as companion
    try {
      await navigator.clipboard.writeText(shareUrl);
    } catch (e) {}

    // Open guidance modal with image preview and copy/download
    showImageShareModal(pngUrl, blob, teamTitle, copied, slug);
  }

  function showKakaoLinkShareModal(teamTitle, shareUrl, slug) {
    const modalRoot = document.getElementById('modal-root');
    if (!modalRoot) return;

    modalRoot.innerHTML = `
      <div class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-slate-950/85 backdrop-blur-sm animate-fade-in" onclick="if(event.target === this) window.app.closeModal()">
        <div class="relative w-full max-w-md bg-slate-900 border border-slate-700/80 rounded-2xl shadow-2xl p-5 sm:p-6 overflow-hidden max-h-[92vh] flex flex-col">
          <div class="flex items-center justify-between pb-3 border-b border-slate-800">
            <div class="flex items-center gap-2">
              <span class="text-xl">💬</span>
              <h3 class="text-base sm:text-lg font-black text-slate-100">카카오톡 링크 공유</h3>
            </div>
            <button onclick="window.app.closeModal()" class="text-slate-400 hover:text-slate-200 text-xl font-bold p-1">✕</button>
          </div>

          <div class="my-4 space-y-3.5">
            <div class="p-3.5 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs sm:text-sm font-semibold flex items-center gap-2.5">
              <span class="text-xl">🔗</span>
              <div>
                <div class="font-black text-emerald-200">공유 링크가 클립보드에 복사되었습니다!</div>
                <div class="text-xs text-emerald-400/90 mt-0.5">카톡 대화창에 <strong>Ctrl + V</strong>(붙여넣기) 하면 썸네일 미리보기가 표시됩니다.</div>
              </div>
            </div>

            <!-- Preview Card (shows how KakaoTalk renders the link with OG image) -->
            <div class="rounded-xl border border-slate-800 bg-slate-950 p-3 space-y-2">
              <div class="text-[11px] text-slate-400 font-bold uppercase tracking-wider">카카오톡 미리보기 카드</div>
              <div class="rounded-lg overflow-hidden border border-slate-800 bg-slate-900">
                <img src="/og-image.png" alt="전술판 썸네일" class="w-full h-32 object-cover" />
                <div class="p-2.5">
                  <div class="text-xs font-bold text-slate-100">${escapeHtml(teamTitle)}</div>
                  <div class="text-[11px] text-slate-400 mt-0.5 line-clamp-1">ALL-TIME XI 역대 국가대표 최강 베스트11 전술판</div>
                  <div class="text-[10px] text-amber-400/80 mt-1">${escapeHtml(shareUrl)}</div>
                </div>
              </div>
            </div>
          </div>

          <div class="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
            <button onclick="window.app.copyShareUrl('${escapeHtml(shareUrl)}')" class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-bold border border-slate-700 transition flex items-center gap-1">
              <span>📋 링크 다시 복사</span>
            </button>
            <div class="flex items-center gap-2">
              <button onclick="window.app.launchPcKakaoTalk()" class="px-3.5 py-2 rounded-xl bg-yellow-400 hover:bg-yellow-300 text-slate-950 text-xs sm:text-sm font-black shadow-lg shadow-yellow-400/20 transition flex items-center gap-1.5">
                <span>💬 카카오톡 열기</span>
              </button>
              <button onclick="window.app.closeModal()" class="px-3 py-2 rounded-xl bg-slate-950 hover:bg-slate-800 text-slate-400 text-xs sm:text-sm font-semibold border border-slate-800">
                닫기
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  async function shareLineupDirectly() {
    const filled = state.builderSlots.filter(s => s.player).length;
    if (filled < 11) {
      const proceed = confirm(`현재 11명 중 ${filled}명만 배치되어 있습니다.
이 상태로 전술판을 카카오톡으로 공유하시겠습니까?`);
      if (!proceed) return;
    }

    showToast('카카오톡 공유 링크를 생성하는 중입니다...', 'info');

    let shareUrl = window.location.href;
    let teamTitle = state.builderTeamName || `${state.builderCountryCode} 역대 최강 베스트11`;
    let slug = '';
    try {
      const res = await saveCurrentLineup(true);
      if (res && res.share_slug) {
        slug = res.share_slug;
        shareUrl = `${window.location.origin}/team/${res.share_slug}`;
        if (res.lineup && res.lineup.team_name) {
          teamTitle = res.lineup.team_name;
        }
      }
    } catch (e) {
      console.warn('Auto-save error before share:', e);
    }

    await copyShareUrl(shareUrl);

    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    if (isMobile && navigator.share) {
      try {
        await navigator.share({
          title: `[ALL-TIME XI] ${teamTitle}`,
          text: `${teamTitle} — 내가 만든 국가대표 역대 최강 베스트11 전술판을 확인하세요!`,
          url: shareUrl
        });
        return;
      } catch (err) {
        if (err.name === 'AbortError') return;
      }
    }

    showKakaoLinkShareModal(teamTitle, shareUrl, slug);
  }

      async function exportCurrentLineupPng(layout = 'portrait', scale = 2) {
    showToast('고해상도 공식 베스트11 포스터 이미지를 준비 중입니다...', 'info');

    // 1. Obtain verified share slug by auto-saving if needed
    const slug = await ensureLineupSaved();
    if (slug) {
      try {
        const downloadUrl = `/api/lineups/${slug}/png?layout=${layout}&scale=${scale}&download=1`;
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = `ALL-TIME-XI-${state.builderCountryCode || 'TEAM'}-${layout}.png`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast('✅ 고해상도 공식 베스트11 포스터 이미지가 저장되었습니다!', 'success');
        return;
      } catch (e) {
        console.warn('Server PNG download error:', e);
      }
    }

    // 2. Client-side fallback if server fails
    const pitchEl = document.getElementById('tactical-pitch-board');
    if (window.html2canvas && pitchEl) {
      try {
        const canvas = await window.html2canvas(pitchEl, {
          scale: 2.0,
          useCORS: true,
          allowTaint: false,
          backgroundColor: '#070b14',
          logging: false
        });
        const dataUrl = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = `ALL-TIME-XI-${state.builderCountryCode || 'TEAM'}-pitch.png`;
        document.body.appendChild(a);
        a.click();
        a.remove();
        showToast('전술판 이미지가 저장되었습니다!', 'success');
        return;
      } catch (err) {
        console.warn('Client fallback capture error:', err);
      }
    }

    const payload = buildLineupPayload();
    if (!payload) return;
    showToast('고해상도 전술판 PNG 이미지를 생성하는 중입니다...', 'info');
    try {
      const resp = await fetch(`/api/export/lineup-png?layout=${encodeURIComponent(layout)}&scale=${scale}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.detail || '이미지 생성 실패');
      }
      const blob = await resp.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `ALL-TIME-XI-${state.builderCountryCode}-${layout}.png`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      setTimeout(() => URL.revokeObjectURL(url), 5000);
      showToast('PNG 이미지 다운로드가 완료되었습니다!', 'success');
    } catch (e) {
      showToast(e.message, 'error');
    }
  }

  async function loadSavedLineupIntoBuilder(slug) {
    try {
      const resp = await fetch(`/api/lineups/${encodeURIComponent(slug)}`);
      if (!resp.ok) throw new Error('저장된 베스트11을 찾을 수 없습니다.');
      const snap = await resp.json();
      state.builderCountryCode = snap.country_fifa_code;
      await loadCountryPlayersForBuilder(snap.country_fifa_code);
      state.builderFormationCode = snap.formation_code;
      state.builderTeamName = snap.team_name;
      state.builderTacticalStyle = snap.tactical_style || '균형형';
      state.builderBoardTheme = snap.board_color_theme || 'classic_emerald';
      state.builderDescription = snap.team_description || '';
      state.builderCaptainId = snap.captain_player_id;

      initBuilderSlotsForFormation(snap.formation_code, false);
      (snap.players || []).forEach(sp => {
        const targetSlot = state.builderSlots[sp.slot_index];
        if (targetSlot) {
          const fullPlayer = state.builderCountryPlayers.find(p => p.id === sp.player_id) || {
            id: sp.player_id,
            player_id: sp.player_id,
            name_ko: sp.name_ko,
            name_en: sp.name_en,
            primary_position: sp.primary_position,
            official_caps: sp.official_caps,
            official_goals: sp.official_goals,
            active_period_label: sp.active_period_label,
            image_url: sp.image_url,
            jersey_number: sp.jersey_number
          };
          targetSlot.player = fullPlayer;
          targetSlot.is_captain = Boolean(sp.is_captain);
          targetSlot.suitability = computeClientSuitability(fullPlayer, targetSlot);
        }
      });

      state.lastSavedLineupResult = {
        share_slug: slug,
        share_url: `/team/${slug}`,
        png_portrait_url: `/api/lineups/${slug}/png?layout=portrait`,
        png_landscape_url: `/api/lineups/${slug}/png?layout=landscape`,
        lineup: snap
      };
      state.view = 'builder';
      render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
      showToast(e.message, 'error');
    }
  }

  async function loadDatabasePlayers() {
    const q = new URLSearchParams();
    if (state.dbCountryCode && state.dbCountryCode !== 'ALL') q.set('country_code', state.dbCountryCode);
    if (state.dbSearch.trim()) q.set('search', state.dbSearch.trim());
    if (state.dbDecade !== 'all') q.set('decade', state.dbDecade);
    if (state.dbPosition !== 'all') q.set('position', state.dbPosition);
    if (state.dbActiveStatus !== 'all') q.set('active_status', state.dbActiveStatus);
    q.set('sort_by', state.dbSortBy);
    q.set('eligible_only', 'true');
    q.set('limit', '240');

    const resp = await fetch(`/api/players?${q.toString()}`);
    const data = await resp.json();
    state.dbPlayers = data.players || [];
    if (state.view === 'database') render();
  }

  // Expose public handler methods on window.app
  window.app = {
    async init() {
      try {
        const bResp = await fetch('/api/bootstrap');
        if (bResp.ok) {
          const bData = await bResp.json();
          state.countries = bData.countries || [];
          state.rankingDate = bData.ranking_snapshot_date || '2026-10-07';
          state.formations = (bData.formations && bData.formations.length) ? bData.formations : DEFAULT_FORMATIONS;
          state.savedLineups = bData.lineups || [];
          if (bData.visitor_stats) updateVisitorCounterUI(bData.visitor_stats);
          trackDailyUniqueVisit();
          state.builderCountryCode = 'BRA';
          state.builderCountryPlayers = bData.initial_builder_players || [];
          initBuilderSlotsForFormation('4-3-3', false);
          autoFillBuilderLegendXI();
        } else {
          throw new Error('Bootstrap fallback');
        }
      } catch (err) {
        try {
          const [cResp, fResp, lResp] = await Promise.all([
            fetch('/api/countries'),
            fetch('/api/formations'),
            fetch('/api/lineups')
          ]);
          const cData = await cResp.json();
          const fData = await fResp.json();
          const lData = await lResp.json();
          state.countries = cData.countries || [];
          state.rankingDate = cData.ranking_snapshot_date || '2026-10-07';
          state.formations = (fData.formations && fData.formations.length) ? fData.formations : DEFAULT_FORMATIONS;
          state.savedLineups = lData.lineups || [];
          await loadCountryPlayersForBuilder('BRA');
          initBuilderSlotsForFormation('4-3-3', false);
          autoFillBuilderLegendXI();
        } catch (e) {
          state.formations = DEFAULT_FORMATIONS;
          initBuilderSlotsForFormation('4-3-3', false);
        }
      }

      // Check if opened via a direct Share URL (/team/{slug})
      const shareCtx = window.__INITIAL_SHARE_CONTEXT__;
      if (shareCtx && shareCtx.type === 'team' && shareCtx.slug) {
        await loadSavedLineupIntoBuilder(shareCtx.slug);
        showToast('공유된 베스트11 전술판을 불러왔습니다!', 'info');
        return;
      }

      render();
    },

    async navigate(view) {
      if (view === 'arena') view = 'builder';
      state.view = view;
      if (view === 'database' && state.dbPlayers.length === 0) {
        await loadDatabasePlayers();
      } else if (view === 'quality' && !state.qualityReport) {
        const r = await fetch('/api/data-quality');
        state.qualityReport = await r.json();
      } else if (view === 'admin') {
        const r = await fetch('/api/admin/audit-logs');
        const d = await r.json();
        state.adminLogs = d.logs || [];
      }
      render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },

    setHeroPreset(idx) {
      state.heroPresetIdx = idx;
      render();
    },

    onHomeSearch(val) {
      state.homeSearch = val;
      render();
      const input = document.querySelector('input[placeholder^="국가명 검색"]');
      if (input) {
        input.focus();
        input.setSelectionRange(val.length, val.length);
      }
    },

    onHomeConfed(cf) {
      state.homeConfed = cf;
      render();
    },

    startCountryBuilder,
    loadSavedLineupIntoBuilder,
    autoFillBuilderLegendXI,

    clearBuilderSlots() {
      state.builderSlots.forEach(s => {
        s.player = null;
        s.suitability = null;
        s.is_captain = false;
      });
      state.builderCaptainId = null;
      state.lastSavedLineupResult = null;
      render();
    },

    changeBuilderFormation(code) {
      initBuilderSlotsForFormation(code, true);
      state.lastSavedLineupResult = null;
      render();
      showToast(`포메이션이 ${code}로 변경되었습니다.`, 'info');
    },

    onBuilderMetaChange(field, val) {
      if (field === 'teamName') state.builderTeamName = val;
      if (field === 'tacticalStyle') state.builderTacticalStyle = val;
      if (field === 'boardTheme') {
        state.builderBoardTheme = val;
        render();
      }
      if (field === 'description') state.builderDescription = val;
    },

    onPitchSlotClick(slotIdx) {
      if (state.swapSourceSlotIndex !== null) {
        if (state.swapSourceSlotIndex !== slotIdx) {
          window.app.swapTwoSlots(state.swapSourceSlotIndex, slotIdx);
        } else {
          state.swapSourceSlotIndex = null;
          render();
        }
        return;
      }
      state.activeSlotIndex = slotIdx;
      state.candPosFilter = 'slot';
      state.candSortBy = 'caps_desc';
      state.candSearch = '';
      render();
      const slotObj = state.builderSlots[slotIdx];
      if (slotObj) {
        showToast(`[${slotObj.slot_code}] ${slotObj.label_ko} 포지션의 A매치 최다 출전 순 추천 선수를 표시합니다.`, 'info');
      }
      const drawer = document.getElementById('builder-candidate-drawer');
      if (drawer && window.innerWidth < 1024) {
        drawer.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },

    showPositionRecommendedCaps() {
      state.candSearch = '';
      state.candPosFilter = 'slot';
      state.candSortBy = 'caps_desc';
      render();
    },

    focusDirectPlayerSearch() {
      state.candPosFilter = 'all';
      render();
      const input = document.getElementById('builder-cand-search-input');
      if (input) {
        input.focus();
      }
    },

    startSwapSlot(slotIdx) {
      state.swapSourceSlotIndex = slotIdx;
      render();
      showToast('교체할 다른 포지션 슬롯을 전술판이나 목록에서 클릭하세요.', 'info');
    },

    cancelSwapMode() {
      state.swapSourceSlotIndex = null;
      render();
    },

    swapTwoSlots(idxA, idxB) {
      const slotA = state.builderSlots[idxA];
      const slotB = state.builderSlots[idxB];
      if (!slotA || !slotB) return;
      const tempP = slotA.player;
      slotA.player = slotB.player;
      slotB.player = tempP;
      slotA.suitability = slotA.player ? computeClientSuitability(slotA.player, slotA) : null;
      slotB.suitability = slotB.player ? computeClientSuitability(slotB.player, slotB) : null;
      slotA.is_captain = Boolean(slotA.player && state.builderCaptainId === (slotA.player.id || slotA.player.player_id));
      slotB.is_captain = Boolean(slotB.player && state.builderCaptainId === (slotB.player.id || slotB.player.player_id));
      state.swapSourceSlotIndex = null;
      state.activeSlotIndex = idxB;
      state.lastSavedLineupResult = null;
      render();
      showToast(`${slotA.slot_code} ⇄ ${slotB.slot_code} 선수 위치가 교체되었습니다.`, 'success');
    },

    onPitchSlotDragStart(ev, slotIdx) {
      state.dragSourceSlotIndex = slotIdx;
      if (ev.dataTransfer) {
        ev.dataTransfer.setData('text/plain', String(slotIdx));
      }
    },

    onPitchSlotDrop(ev, targetIdx) {
      ev.preventDefault();
      const srcIdx = state.dragSourceSlotIndex !== null ? state.dragSourceSlotIndex : Number(ev.dataTransfer.getData('text/plain'));
      state.dragSourceSlotIndex = null;
      if (!Number.isNaN(srcIdx) && srcIdx !== targetIdx) {
        window.app.swapTwoSlots(srcIdx, targetIdx);
      }
    },

    assignPlayerToActiveSlot(playerId) {
      // Check duplicate (Test F)
      const duplicateSlot = state.builderSlots.find(s => s.player && (s.player.id === playerId || s.player.player_id === playerId));
      if (duplicateSlot) {
        showToast('같은 선수를 하나의 베스트11에 두 번 배치할 수 없습니다.', 'error');
        return;
      }
      const pObj = state.builderCountryPlayers.find(p => p.id === playerId);
      if (!pObj) return;
      const slot = state.builderSlots[state.activeSlotIndex];
      if (!slot) return;
      slot.player = pObj;
      slot.suitability = computeClientSuitability(pObj, slot);
      if (!state.builderCaptainId) {
        state.builderCaptainId = pObj.id;
        slot.is_captain = true;
      }
      // Advance activeSlotIndex to next empty slot if any
      const nextEmpty = state.builderSlots.findIndex(s => !s.player);
      if (nextEmpty !== -1) state.activeSlotIndex = nextEmpty;
      state.lastSavedLineupResult = null;
      render();
      if (slot.suitability.isLow) {
        showToast(`${formatNameKoEn(pObj)} 선수가 ${slot.slot_code}에 배치되었습니다. (주의: 포지션 적합도 낮음)`, 'warn');
      } else {
        showToast(`${formatNameKoEn(pObj)} 선수가 [${slot.slot_code}] 포지션에 배치되었습니다.`, 'success');
      }
    },

    removePlayerFromSlot(slotIdx) {
      const slot = state.builderSlots[slotIdx];
      if (!slot) return;
      slot.player = null;
      slot.suitability = null;
      slot.is_captain = false;
      state.activeSlotIndex = slotIdx;
      state.lastSavedLineupResult = null;
      render();
    },

    setCaptain(playerId) {
      state.builderCaptainId = playerId;
      state.builderSlots.forEach(s => {
        s.is_captain = Boolean(s.player && (s.player.id === playerId || s.player.player_id === playerId));
      });
      render();
      showToast('주장(Captain)이 변경되었습니다.', 'info');
    },

    setCandPosFilter(val) {
      state.candPosFilter = val;
      if (val === 'slot') {
        state.candSortBy = 'caps_desc';
      }
      render();
    },

    onCandSearch(val) {
      state.candSearch = val;
      render();
      const input = document.getElementById('builder-cand-search-input');
      if (input) {
        input.focus();
        input.setSelectionRange(val.length, val.length);
      }
    },

    onCandFilter(field, val) {
      if (field === 'decade') state.candDecade = val;
      if (field === 'activeStatus') state.candActiveStatus = val;
      if (field === 'sortBy') state.candSortBy = val;
      render();
    },

    saveCurrentLineup,
    shareLineupDirectly,
    shareSavedLineupDirectly,
    exportCurrentLineupPng,
    shareLineupImageDirectly,
    copyImageToClipboard,
    shareImageViaNativeShare,

    async onDbFilter(field, val) {
      if (field === 'country') state.dbCountryCode = val;
      if (field === 'search') state.dbSearch = val;
      if (field === 'position') state.dbPosition = val;
      if (field === 'decade') state.dbDecade = val;
      if (field === 'activeStatus') state.dbActiveStatus = val;
      if (field === 'sortBy') state.dbSortBy = val;
      await loadDatabasePlayers();
      if (field === 'search') {
        const input = document.querySelector('input[placeholder^="선수 이름·영문·별칭"]');
        if (input) {
          input.focus();
          input.setSelectionRange(val.length, val.length);
        }
      }
    },

    openPlayerModal,
    closeModal,

    async copyShareUrl(url) {
      try {
        await navigator.clipboard.writeText(url);
        showToast('공유 URL이 클립보드에 복사되었습니다!', 'success');
      } catch (e) {
        prompt('아래 공유 URL을 복사하세요:', url);
      }
    },

    async shareNativeOrKakao(title, url) {
      if (navigator.share) {
        try {
          await navigator.share({ title: `[ALL-TIME XI] ${title}`, text: `${title} — 역대 국가대표 베스트11 전술판을 확인하세요!`, url });
          return;
        } catch (e) {}
      }
      await window.app.copyShareUrl(url);
      showToast('링크가 복사되었습니다. 카카오톡이나 SNS 대화창에 붙여넣어 공유하세요!', 'info');
    },

    async submitAdminPlayer() {
      const pidVal = document.getElementById('adm-pid').value;
      const payload = {
        player_id: pidVal ? Number(pidVal) : null,
        country_fifa_code: document.getElementById('adm-country').value,
        name_ko: document.getElementById('adm-name-ko').value,
        name_en: document.getElementById('adm-name-en').value,
        primary_position: document.getElementById('adm-pos').value,
        official_caps: Number(document.getElementById('adm-caps').value),
        official_goals: Number(document.getElementById('adm-goals').value),
        career_start_year: Number(document.getElementById('adm-y1').value),
        career_end_year: Number(document.getElementById('adm-y2').value),
        image_url: document.getElementById('adm-img').value || null,
        license_info: document.getElementById('adm-lic').value || null,
        admin_note: document.getElementById('adm-note').value
      };
      try {
        const resp = await fetch('/api/admin/players', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || '저장 실패');
        showToast(`선수 데이터(ID #${data.player_id})가 저장되었습니다.`, 'success');
        await window.app.navigate('admin');
      } catch (e) {
        showToast(e.message, 'error');
      }
    },

    async submitAdminMerge() {
      const keepId = Number(document.getElementById('adm-merge-keep').value);
      const remId = Number(document.getElementById('adm-merge-rem').value);
      try {
        const resp = await fetch('/api/admin/merge-players', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ keep_player_id: keepId, remove_player_id: remId })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || '병합 실패');
        showToast(`선수 #${remId} 데이터가 #${keepId}로 병합되었습니다.`, 'success');
        await window.app.navigate('admin');
      } catch (e) {
        showToast(e.message, 'error');
      }
    },

    async submitAdminCsv() {
      const fileInput = document.getElementById('adm-csv-file');
      if (!fileInput || !fileInput.files.length) {
        showToast('업로드할 CSV 파일을 선택해 주세요.', 'warn');
        return;
      }
      const fd = new FormData();
      fd.append('file', fileInput.files[0]);
      try {
        const resp = await fetch('/api/admin/import-csv', { method: 'POST', body: fd });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'CSV 가져오기 실패');
        showToast(`CSV에서 ${data.imported_rows}명의 선수 레코드를 가져왔습니다.`, 'success');
        await window.app.navigate('admin');
      } catch (e) {
        showToast(e.message, 'error');
      }
    }
  };

  document.addEventListener('DOMContentLoaded', () => {
    window.app.init();
  });
})();
