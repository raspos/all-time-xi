-- ALL-TIME XI Relational Database Schema (SQLite / PostgreSQL compatible)

PRAGMA foreign_keys = ON;

-- 1. countries (국가 마스터 테이블)
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fifa_code TEXT NOT NULL UNIQUE,
    iso_alpha2 TEXT,
    name_ko TEXT NOT NULL,
    name_en TEXT NOT NULL,
    confederation TEXT NOT NULL,
    flag_emoji TEXT NOT NULL,
    flag_svg_url TEXT,
    world_cup_titles INTEGER NOT NULL DEFAULT 0,
    world_cup_winning_years TEXT,
    major_honors_ko TEXT,
    kit_primary_color TEXT NOT NULL DEFAULT '#1e293b',
    kit_secondary_color TEXT NOT NULL DEFAULT '#ffffff',
    kit_accent_color TEXT NOT NULL DEFAULT '#fbbf24',
    kit_text_color TEXT NOT NULL DEFAULT '#ffffff',
    kit_pattern_type TEXT NOT NULL DEFAULT 'solid', -- solid, stripes, hoops, sash, halves
    historical_note_ko TEXT,
    tm_national_team_id INTEGER,
    rsssf_url TEXT,
    wiki_list_url TEXT,
    data_coverage_note_ko TEXT,
    last_data_updated_at TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 2. country_ranking_snapshots (FIFA 세계랭킹 스냅샷 테이블 - 국가 마스터와 분리)
CREATE TABLE IF NOT EXISTS country_ranking_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    snapshot_date TEXT NOT NULL, -- e.g. '2026-10-07'
    country_id INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    fifa_rank INTEGER NOT NULL,
    rank_change INTEGER DEFAULT 0,
    fifa_points REAL NOT NULL,
    is_target_top30 INTEGER NOT NULL DEFAULT 1,
    is_current_snapshot INTEGER NOT NULL DEFAULT 1,
    official_source_url TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    UNIQUE(snapshot_date, country_id)
);

-- 2b. country_succession_mappings (역대 국가대표팀 기록 승계 매핑 테이블)
CREATE TABLE IF NOT EXISTS country_succession_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    historical_team_code TEXT NOT NULL,
    historical_team_name_ko TEXT NOT NULL,
    historical_team_name_en TEXT NOT NULL,
    modern_country_id INTEGER REFERENCES countries(id) ON DELETE SET NULL,
    modern_fifa_code TEXT,
    is_auto_merged INTEGER NOT NULL DEFAULT 0, -- 1 for FRG->GER, 0 for URS/YUG/TCH
    policy_rule_ko TEXT NOT NULL,
    fifa_recognition_note_ko TEXT NOT NULL
);

-- 3. players (선수 마스터 테이블 - 내부 고유 ID 사용)
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    internal_uid TEXT NOT NULL UNIQUE, -- e.g. 'PLR-BRA-PELE-1940'
    name_ko TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_native TEXT,
    aliases_search TEXT, -- comma/space separated aliases for instant search
    nationality_code TEXT NOT NULL,
    date_of_birth TEXT,
    birth_year INTEGER,
    is_deceased INTEGER, -- NULL if unknown, 0 if alive, 1 if deceased
    date_of_death TEXT,
    primary_position TEXT NOT NULL, -- GK, CB, LB, RB, CDM, CM, CAM, LW, RW, ST
    position_group TEXT NOT NULL, -- GK, DF, MF, FW
    secondary_positions TEXT, -- JSON array or comma-separated e.g. '["CAM","RW"]'
    height_cm INTEGER,
    preferred_foot TEXT, -- 'right', 'left', 'both', or NULL
    is_active_player INTEGER NOT NULL DEFAULT 0, -- 1 현역, 0 은퇴
    play_style_ko TEXT,
    primary_role_ko TEXT,
    attack_defense_traits_ko TEXT,
    work_rate_mobility_ko TEXT,
    tactical_fit_role_ko TEXT,
    fact_bio_ko TEXT,
    ai_style_summary_ko TEXT,
    is_legend_test_case INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 4. player_national_team_careers (국가별 성인 남자 A대표팀 출전/득점 기록 - 복수 국가 분리 저장)
CREATE TABLE IF NOT EXISTS player_national_team_careers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    country_id INTEGER NOT NULL REFERENCES countries(id) ON DELETE CASCADE,
    represented_fifa_code TEXT NOT NULL,
    historical_team_code TEXT, -- e.g. 'FRG' for West Germany
    career_start_year INTEGER,
    career_end_year INTEGER,
    active_period_label TEXT, -- e.g. '1957–1971'
    decade_tags TEXT, -- JSON array e.g. '["1950s","1960s","1970s"]'
    primary_decade TEXT, -- e.g. '1960s'
    official_caps INTEGER, -- NULL if unverified
    official_goals INTEGER,
    is_eligible_30_caps INTEGER NOT NULL DEFAULT 0, -- 1 if official_caps >= 30
    verification_status TEXT NOT NULL DEFAULT 'verified', -- 'verified', 'pending_verification', 'excluded_under_30'
    record_source_name TEXT NOT NULL,
    record_source_url TEXT,
    verified_date TEXT NOT NULL,
    discrepancy_note_ko TEXT,
    UNIQUE(player_id, country_id, represented_fifa_code)
);

-- 5. player_positions (선수 포지션 및 세부 슬롯 적합도 테이블)
CREATE TABLE IF NOT EXISTS player_positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    position_code TEXT NOT NULL, -- GK, CB, LCB, RCB, LB, RB, LWB, RWB, CDM, LDM, RDM, CM, LCM, RCM, CAM, LAM, RAM, LM, RM, LW, RW, LF, RF, CF, ST, LS, RS
    position_group TEXT NOT NULL, -- GK, DF, MF, FW
    is_primary INTEGER NOT NULL DEFAULT 0,
    suitability_tier TEXT NOT NULL DEFAULT 'natural', -- 'natural' (100), 'secondary' (85), 'adaptable' (65)
    suitability_score INTEGER NOT NULL DEFAULT 100,
    UNIQUE(player_id, position_code)
);

-- 6. player_career_awards (선수 주요 클럽 및 수상 경력 테이블)
CREATE TABLE IF NOT EXISTS player_career_awards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL UNIQUE REFERENCES players(id) ON DELETE CASCADE,
    major_clubs_ko TEXT, -- JSON or comma list of major clubs
    major_honors_ko TEXT, -- 대표 수상 및 우승 요약
    world_cup_participations TEXT, -- e.g. '1958, 1962, 1966, 1970'
    world_cup_winner INTEGER, -- 1, 0, or NULL
    world_cup_titles_count INTEGER DEFAULT 0,
    continental_winner INTEGER, -- 1, 0, or NULL
    continental_titles_ko TEXT,
    ballon_dor_winner INTEGER, -- 1, 0, or NULL
    ballon_dor_count INTEGER DEFAULT 0,
    individual_awards_ko TEXT
);

-- 7. player_images (선수 사진 및 라이선스 정보 테이블)
CREATE TABLE IF NOT EXISTS player_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL UNIQUE REFERENCES players(id) ON DELETE CASCADE,
    image_url TEXT,
    original_source_name TEXT,
    original_source_url TEXT,
    license_info TEXT, -- e.g. 'CC BY-SA 4.0', 'Public Domain', 'Transfermarkt Profile Ref'
    requires_attribution INTEGER DEFAULT 0,
    author_credit TEXT,
    fallback_number INTEGER DEFAULT 10,
    fallback_initials TEXT
);

-- 8. data_sources (데이터 출처 마스터 테이블)
CREATE TABLE IF NOT EXISTS data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_code TEXT NOT NULL UNIQUE,
    source_name TEXT NOT NULL,
    base_url TEXT NOT NULL,
    coverage_scope_ko TEXT NOT NULL,
    last_updated_date TEXT NOT NULL,
    terms_and_license_ko TEXT NOT NULL,
    collection_method_ko TEXT NOT NULL
);

-- 9. player_source_records (선수별 외부 데이터 출처 매핑 및 원자료 기록 테이블)
CREATE TABLE IF NOT EXISTS player_source_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    source_id INTEGER NOT NULL REFERENCES data_sources(id) ON DELETE CASCADE,
    external_id TEXT,
    external_url TEXT,
    source_caps INTEGER,
    source_goals INTEGER,
    source_position TEXT,
    raw_excerpt_json TEXT,
    checked_at TEXT NOT NULL,
    UNIQUE(player_id, source_id)
);

-- 10. data_quality_flags (데이터 품질 검사 및 불일치 플래그 테이블)
CREATE TABLE IF NOT EXISTS data_quality_flags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER REFERENCES players(id) ON DELETE CASCADE,
    country_id INTEGER REFERENCES countries(id) ON DELETE CASCADE,
    flag_type TEXT NOT NULL, -- 'caps_discrepancy', 'era_gap_warning', 'missing_photo', 'position_inferred', 'pending_caps_check'
    severity TEXT NOT NULL DEFAULT 'info', -- 'info', 'warning', 'high'
    description_ko TEXT NOT NULL,
    source_a_value TEXT,
    source_b_value TEXT,
    is_resolved INTEGER NOT NULL DEFAULT 0,
    resolved_note_ko TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    resolved_at TEXT
);

-- 11. formations (전술 포메이션 마스터 테이블)
CREATE TABLE IF NOT EXISTS formations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE, -- '4-3-3', '4-2-3-1', '4-4-2', '4-1-4-1', '3-5-2', '3-4-3', '4-2-2-2'
    name_ko TEXT NOT NULL,
    description_ko TEXT NOT NULL,
    tactical_characteristics_ko TEXT NOT NULL,
    slots_json TEXT NOT NULL -- JSON array of 11 slots: slot_index, slot_code, label_ko, group, x, y, compatible_positions
);

-- 12. users (선택적 사용자 테이블)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_token TEXT NOT NULL UNIQUE,
    nickname TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 13. saved_lineups (사용자 저장 베스트11 테이블)
CREATE TABLE IF NOT EXISTS saved_lineups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    share_slug TEXT NOT NULL UNIQUE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    country_id INTEGER NOT NULL REFERENCES countries(id),
    country_fifa_code TEXT NOT NULL,
    country_name_ko TEXT NOT NULL,
    team_name TEXT NOT NULL,
    formation_code TEXT NOT NULL,
    captain_player_id INTEGER REFERENCES players(id) ON DELETE SET NULL,
    tactical_style TEXT NOT NULL DEFAULT '균형형',
    board_color_theme TEXT NOT NULL DEFAULT 'classic_emerald',
    team_description TEXT,
    lineup_snapshot_json TEXT NOT NULL, -- Full immutable snapshot so ranking/player updates never break saved lineups
    view_count INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 14. lineup_players (베스트11 배치 선수 상세 테이블)
CREATE TABLE IF NOT EXISTS lineup_players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lineup_id INTEGER NOT NULL REFERENCES saved_lineups(id) ON DELETE CASCADE,
    slot_index INTEGER NOT NULL,
    slot_code TEXT NOT NULL,
    player_id INTEGER NOT NULL REFERENCES players(id),
    custom_x REAL,
    custom_y REAL,
    suitability_status TEXT NOT NULL, -- '적합', '부포지션 적합', '포지션 적합도 낮음'
    suitability_score INTEGER NOT NULL DEFAULT 100,
    jersey_number INTEGER,
    is_captain INTEGER NOT NULL DEFAULT 0,
    UNIQUE(lineup_id, slot_index),
    UNIQUE(lineup_id, player_id)
);

-- 15. ai_comparisons (AI 가상 대결 분석 및 스냅샷 저장 테이블)
CREATE TABLE IF NOT EXISTS ai_comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    share_slug TEXT NOT NULL UNIQUE,
    cache_key TEXT NOT NULL UNIQUE,
    team_a_lineup_id INTEGER REFERENCES saved_lineups(id) ON DELETE SET NULL,
    team_b_lineup_id INTEGER REFERENCES saved_lineups(id) ON DELETE SET NULL,
    team_a_snapshot_json TEXT NOT NULL,
    team_b_snapshot_json TEXT NOT NULL,
    provider_name TEXT NOT NULL, -- 'gemini', 'openai'
    model_name TEXT NOT NULL,
    analysis_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- 16. admin_audit_logs (관리자 데이터 수정 이력 테이블)
CREATE TABLE IF NOT EXISTS admin_audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL, -- 'create_player', 'update_player', 'update_caps', 'merge_players', 'update_image', 'import_csv', 'update_ranking', 'resolve_flag'
    target_table TEXT NOT NULL,
    target_id TEXT,
    before_json TEXT,
    after_json TEXT,
    admin_note TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_players_nationality ON players(nationality_code);
CREATE INDEX IF NOT EXISTS idx_players_position ON players(primary_position);
CREATE INDEX IF NOT EXISTS idx_players_group ON players(position_group);
CREATE INDEX IF NOT EXISTS idx_nt_careers_country_caps ON player_national_team_careers(country_id, is_eligible_30_caps, official_caps DESC);
CREATE INDEX IF NOT EXISTS idx_nt_careers_player ON player_national_team_careers(player_id);
CREATE INDEX IF NOT EXISTS idx_quality_flags_country ON data_quality_flags(country_id, flag_type);
