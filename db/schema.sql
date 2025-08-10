-- ----------------------------------------------------
-- races: レース基本情報
-- ----------------------------------------------------
CREATE TABLE races (
    race_id BIGINT PRIMARY KEY COMMENT 'レースID（例:202507020311）',
    date DATE NOT NULL COMMENT '開催日',
    start_time DATETIME COMMENT '発走時刻',
    venue VARCHAR(50) NOT NULL COMMENT '競馬場名',
    race_number INT NOT NULL COMMENT 'レース番号',
    distance INT COMMENT '距離(m)',
    track_type VARCHAR(10) COMMENT '芝・ダートなど',
    course_shape VARCHAR(10) COMMENT '右回り・左回りなど',
    track_condition VARCHAR(20) COMMENT '馬場状態（良・稍重など）',
    race_class VARCHAR(50) COMMENT 'G1などのクラス',
    num_of_horses INT COMMENT '出走頭数'
);

-- ----------------------------------------------------
-- horses: 馬情報
-- ----------------------------------------------------
CREATE TABLE horses (
    horse_id BIGINT PRIMARY KEY COMMENT '馬ID（例:2022105718）',
    name VARCHAR(100) NOT NULL COMMENT '馬名',
    birth_date DATE COMMENT '生年月日',
    sex TINYINT NOT NULL COMMENT '性別 1=牡,2=牝,3=セン',
    trainer_id BIGINT COMMENT '調教師ID',
    sire VARCHAR(100) COMMENT '父馬',
    dam VARCHAR(100) COMMENT '母馬',
    breeder VARCHAR(100) COMMENT '生産者（例:ノーザンファーム）',
    owner VARCHAR(100) COMMENT '馬主',
    base_running_style VARCHAR(10) COMMENT '基本脚質（逃・先・差・追）',
    career_earnings_jra INT COMMENT '中央での獲得賞金（円）',
    career_earnings_local INT COMMENT '地方での獲得賞金（円）',
    FOREIGN KEY (trainer_id) REFERENCES trainers(trainer_id)
);

-- ----------------------------------------------------
-- trainers: 調教師情報
-- ----------------------------------------------------
CREATE TABLE trainers (
    trainer_id BIGINT PRIMARY KEY COMMENT '調教師ID',
    name VARCHAR(100) COMMENT '調教師名',
    stable VARCHAR(20) COMMENT '所属（栗東・美浦など）'
);

-- ----------------------------------------------------
-- jockeys: 騎手情報
-- ----------------------------------------------------
CREATE TABLE jockeys (
    jockey_id BIGINT PRIMARY KEY COMMENT '騎手ID',
    name VARCHAR(100) COMMENT '騎手名',
);

-- ----------------------------------------------------
-- entries: 出走情報
-- ----------------------------------------------------
CREATE TABLE entries (
    entry_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL COMMENT 'レースID',
    horse_id BIGINT NOT NULL COMMENT '馬ID',
    jockey_id BIGINT COMMENT '騎手ID',
    frame_no INT COMMENT '枠番',
    horse_no INT COMMENT '馬番',
    weight INT COMMENT '斤量',
    previous_weight INT COMMENT '前走馬体重',
    equipment VARCHAR(50) COMMENT '馬具（例:ブリンカー）',
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id),
    FOREIGN KEY (jockey_id) REFERENCES jockeys(jockey_id)
);

-- ----------------------------------------------------
-- results: レース結果
-- ----------------------------------------------------
CREATE TABLE results (
    race_id BIGINT NOT NULL COMMENT 'レースID',
    horse_id BIGINT NOT NULL COMMENT '馬ID',
    jockey_id BIGINT NOT NULL COMMENT '騎手ID',
    rank INT COMMENT '着順',
    final_time DECIMAL(5,2) COMMENT 'タイム（例:95.3秒）',
    margin VARCHAR(20) COMMENT '着差',
    last3f DECIMAL(4,1) COMMENT '上がり3F',
    weight INT COMMENT '当日馬体重',
    weight_diff INT COMMENT '前走比増減',
    running_style VARCHAR(10) COMMENT 'そのレースでの脚質（逃・先・差・追）',
    corner_passage VARCHAR(50) COMMENT 'コーナー通過順（例:3-4-3-2）',
    trouble_note TEXT COMMENT '出遅れ・不利など',
    PRIMARY KEY (race_id, horse_id),
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);

-- ----------------------------------------------------
-- odds: オッズ履歴
-- ----------------------------------------------------
CREATE TABLE odds (
    odds_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL COMMENT 'レースID',
    horse_id BIGINT NOT NULL COMMENT '馬ID',
    timestamp DATETIME NOT NULL COMMENT '取得時刻',
    odds_type VARCHAR(20) COMMENT '単勝・複勝など',
    odds DECIMAL(5,2) COMMENT 'オッズ値',
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);

-- ----------------------------------------------------
-- weather: 天気履歴
-- ----------------------------------------------------
CREATE TABLE weather (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    race_id BIGINT NOT NULL COMMENT 'レースID',
    timestamp DATETIME NOT NULL COMMENT '取得時刻',
    weather_text VARCHAR(50) COMMENT '天気（晴・曇など）',
    temp DECIMAL(4,1) COMMENT '気温',
    humidity DECIMAL(4,1) COMMENT '湿度',
    wind_kph DECIMAL(4,1) COMMENT '風速(km/h)',
    wind_direction VARCHAR(10) COMMENT '風向',
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);

-- ----------------------------------------------------
-- payouts: 払戻金
-- ----------------------------------------------------
CREATE TABLE payouts (
    payout_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL COMMENT 'レースID',
    bet_type VARCHAR(20) COMMENT '単勝・複勝など',
    combination VARCHAR(50) COMMENT '的中馬番など',
    payout INT COMMENT '払戻金（円）',
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);

-- ----------------------------------------------------
-- workouts: 調教タイム
-- ----------------------------------------------------
CREATE TABLE workouts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    horse_id BIGINT NOT NULL COMMENT '馬ID',
    race_id BIGINT NOT NULL COMMENT '該当レースID',
    date DATE NOT NULL COMMENT '調教日',
    course VARCHAR(50) COMMENT '坂路・南Wなど',
    distance INT COMMENT '調教距離(m)',
    time DECIMAL(4,1) COMMENT '調教タイム',
    jockey VARCHAR(100) COMMENT '調教騎乗者',
    notes TEXT COMMENT 'メモ',
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id),
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);

-- ----------------------------------------------------
-- paddock_comments: パドック評価
-- ----------------------------------------------------
CREATE TABLE paddock_comments (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    race_id BIGINT NOT NULL COMMENT 'レースID',
    horse_id BIGINT NOT NULL COMMENT '馬ID',
    timestamp DATETIME COMMENT '取得時刻',
    comment TEXT COMMENT '評価文やS/A/Bなど',
    source VARCHAR(50) COMMENT 'netkeibaなど',
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);

-- ----------------------------------------------------
-- race_features: パドック評価
-- ----------------------------------------------------
CREATE TABLE race_features (
    race_id BIGINT,
    horse_id BIGINT,
    odds_t30 DECIMAL(5,2),
    odds_t10 DECIMAL(5,2),
    odds_t0 DECIMAL(5,2),
    odds_change_t30_t0 DECIMAL(6,3),
    odds_change_t10_t0 DECIMAL(6,3),
    PRIMARY KEY (race_id, horse_id)
);
