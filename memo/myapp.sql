CREATE TABLE races (
    race_id BIGINT PRIMARY KEY,
    date DATE NOT NULL,
    venue VARCHAR(50) NOT NULL,
    race_number INT NOT NULL,
    distance INT,
    track_type VARCHAR(10),
    course_shape VARCHAR(10),
    track_condition VARCHAR(20)  -- 確定した馬場状態のみ
);

CREATE TABLE weather (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    race_id BIGINT NOT NULL,
    timestamp DATETIME NOT NULL COMMENT '取得時刻',
    weather_text VARCHAR(50),
    temp DECIMAL(4,1),
    humidity DECIMAL(4,1),
    wind_kph DECIMAL(4,1),
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);


CREATE TABLE horses (
    horse_id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    birth_date DATE,
    sex TINYINT NOT NULL comment "1=牡, 2=牝, 3=セン",                    -- 1=牡, 2=牝, 3=セン
    trainer VARCHAR(100),
    stable VARCHAR(20) comment "栗東・美浦など"                        -- 栗東・美浦など
);

CREATE TABLE entries (
    entry_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL,
    horse_id BIGINT NOT NULL,
    jockey VARCHAR(100) comment "騎手",
    frame_no INT comment "枠番",                            -- 枠番
    horse_no INT comment "馬番",                            -- 馬番
    weight INT comment "負荷重量（kg）",                              -- 負担重量
    previous_weight INT comment "前走馬体重",                     -- 前走馬体重
    running_style VARCHAR(20) comment "逃げ・先行・差し・追込など",               -- 逃げ・先行・差し・追込など
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);

CREATE TABLE odds (
    odds_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL,
    horse_id BIGINT NOT NULL,
    timestamp DATETIME NOT NULL comment "オッズ取得時刻",              -- オッズ取得時刻
    odds DECIMAL(5,2) comment "単勝オッズ",
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);


CREATE TABLE results (
    race_id BIGINT NOT NULL,
    horse_id BIGINT NOT NULL,
    rank INT comment "着順",                                  -- 着順
    final_time DECIMAL(5,2) comment "タイム（例: 95.3秒）",                   -- タイム（例: 95.3秒）
    margin VARCHAR(20) comment "着差",                        -- 着差
    last3f DECIMAL(4,1) comment "上がり3Fタイム",                       -- 上がり3Fタイム
    weight INT comment "当日馬体重",                                -- 当日馬体重
    weight_diff INT comment "前走比増減",                           -- 前走比増減
    PRIMARY KEY (race_id, horse_id),
    FOREIGN KEY (race_id) REFERENCES races(race_id),
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id)
);

CREATE TABLE payouts (
    payout_id BIGINT PRIMARY KEY AUTO_INCREMENT,
    race_id BIGINT NOT NULL,
    bet_type VARCHAR(20) comment "単勝・複勝・枠連・馬連・三連単など",                       -- 単勝・複勝・枠連・馬連・三連単など
    combination VARCHAR(50) comment "的中馬番（例：7,13など）",                    -- 的中馬番（例：7,13など）
    payout INT comment "払戻金（円）",                                 -- 払戻金（円）
    FOREIGN KEY (race_id) REFERENCES races(race_id)
);

CREATE TABLE workouts (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '調教タイム一意ID',
    horse_id BIGINT NOT NULL COMMENT '馬ID（horsesテーブルへのFK）',
    race_id BIGINT NOT NULL COMMENT '対象レースID（racesテーブルへのFK）',
    date DATE NOT NULL COMMENT '調教実施日',
    course VARCHAR(50) COMMENT '調教コース（例：南W, 坂路, 芝など）',
    distance INT COMMENT '調教距離（例：800, 1000, 1200など）',
    time DECIMAL(4,1) COMMENT '調教タイム（例：65.2秒）',
    jockey VARCHAR(100) COMMENT '調教騎乗者（騎手名など、任意）',
    notes TEXT COMMENT '調教コメント（例：馬なり・強めなど）',
    FOREIGN KEY (horse_id) REFERENCES horses(horse_id),
    FOREIGN KEY (race_id) REFERENCES races(race_id)
) COMMENT='レース当週の調教タイム記録';

-- 🗂 全体テーブル構成
-- races：レース基本情報

-- horses：馬基本情報

-- entries：レースごとの出走情報

-- odds：単勝オッズの時間別記録

-- results：レース結果

-- payouts：レース後の払い戻し（全券種）

-- weather_snapshots：レース開催日の各会場・時間帯ごとの天気情報

-- ✅ 1️⃣ races（レース基本情報）
-- column	type	note
-- race_id (PK)	bigint	レースID（例：202507210901）
-- date	date	開催日
-- venue	varchar	開催地（例：Tokyo, Hanshinなど）
-- race_number	int	レース番号
-- distance	int	距離（m）
-- track_type	varchar	芝・ダート
-- course_shape	varchar	左回り・右回りなど
-- weather_text	varchar	当日の天候（例：Sunny, Cloudyなど）
-- avg_temp	decimal(4,1)	平均気温
-- max_temp	decimal(4,1)	最高気温
-- min_temp	decimal(4,1)	最低気温
-- avg_humidity	decimal(4,1)	平均湿度
-- max_wind_kph	decimal(4,1)	最大風速
-- track_condition	varchar	良・稍重など

-- ✅ 2️⃣ horses（馬基本情報）
-- column	type	note
-- horse_id (PK)	bigint	馬ID
-- name	varchar	馬名
-- birth_date	date	生年月日（年齢計算用）
-- sex	varchar	性別（牡・牝・センなど）
-- trainer	varchar	調教師名
-- stable	varchar	所属（栗東・美浦など）

-- ✅ 3️⃣ entries（出走情報）
-- column	type	note
-- entry_id (PK)	bigint	
-- race_id (FK)	bigint	
-- horse_id (FK)	bigint	
-- jockey	varchar	騎手名
-- frame_no	int	枠番
-- horse_no	int	馬番
-- weight	int	負担重量（kg）
-- previous_weight	int	前走馬体重（輸送減り分析用）
-- running_style	varchar	脚質（逃げ・先行・差し・追込など）※任意

-- ✅ 4️⃣ odds（単勝オッズ変動記録）
-- column	type	note
-- odds_id (PK)	bigint	
-- race_id (FK)	bigint	
-- horse_id (FK)	bigint	
-- timestamp	datetime	オッズ取得時刻
-- odds	decimal(5,2)	単勝オッズ

-- ※レース前だけ記録（例：朝・昼・直前など複数行）

-- ✅ 5️⃣ results（レース結果）
-- column	type	note
-- race_id (FK)	bigint	
-- horse_id (FK)	bigint	
-- rank	int	着順
-- final_time	decimal(5,2)	タイム（例：95.3秒）
-- margin	varchar	着差（例：クビ・1/2など）
-- last3f	decimal(4,1)	上がり3Fタイム
-- weight	int	当日馬体重
-- weight_diff	int	前走比増減（輸送減り分析用）

-- ✅ 6️⃣ payouts（払い戻し結果）
-- column	type	note
-- payout_id (PK)	bigint	
-- race_id (FK)	bigint	
-- bet_type	varchar	単勝・複勝・枠連・馬連・三連単など
-- combination	varchar	的中馬番（例：7,13など）
-- payout	int	払戻金（円）