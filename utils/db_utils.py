import mysql.connector
from mysql.connector import Error

def get_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='yajima244',
        database='myapp',
        charset='utf8mb4'
    )

# --- INSERT関数例 ---

def insert_race(race):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO races (race_id, date, venue, race_number, distance, track_type, course_shape, track_condition)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date=VALUES(date),
                venue=VALUES(venue),
                race_number=VALUES(race_number),
                distance=VALUES(distance),
                track_type=VALUES(track_type),
                course_shape=VALUES(course_shape),
                track_condition=VALUES(track_condition)
        """
        cursor.execute(sql, (
            race['race_id'],
            race['date'],
            race['venue'],
            race['race_number'],
            race.get('distance'),
            race.get('track_type'),
            race.get('course_shape'),
            race.get('track_condition')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_race: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_horse(horse):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO horses (horse_id, name, birth_date, sex, trainer, stable)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=VALUES(name),
                birth_date=VALUES(birth_date),
                sex=VALUES(sex),
                trainer=VALUES(trainer),
                stable=VALUES(stable)
        """
        cursor.execute(sql, (
            horse['horse_id'],
            horse['name'],
            horse.get('birth_date'),
            horse['sex'],
            horse.get('trainer'),
            horse.get('stable')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_horse: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_entry(entry):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO entries (race_id, horse_id, jockey, frame_no, horse_no, weight, previous_weight, running_style)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                jockey=VALUES(jockey),
                frame_no=VALUES(frame_no),
                horse_no=VALUES(horse_no),
                weight=VALUES(weight),
                previous_weight=VALUES(previous_weight),
                running_style=VALUES(running_style)
        """
        cursor.execute(sql, (
            entry['race_id'],
            entry['horse_id'],
            entry.get('jockey'),
            entry.get('frame_no'),
            entry.get('horse_no'),
            entry.get('weight'),
            entry.get('previous_weight'),
            entry.get('running_style')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_entry: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_odds(odds):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO odds (race_id, horse_id, timestamp, odds)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            odds['race_id'],
            odds['horse_id'],
            odds['timestamp'],
            odds.get('odds')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_odds: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_result(result):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO results (race_id, horse_id, rank, final_time, margin, last3f, weight, weight_diff)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                rank=VALUES(rank),
                final_time=VALUES(final_time),
                margin=VALUES(margin),
                last3f=VALUES(last3f),
                weight=VALUES(weight),
                weight_diff=VALUES(weight_diff)
        """
        cursor.execute(sql, (
            result['race_id'],
            result['horse_id'],
            result.get('rank'),
            result.get('final_time'),
            result.get('margin'),
            result.get('last3f'),
            result.get('weight'),
            result.get('weight_diff')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_result: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_payout(payout):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO payouts (race_id, bet_type, combination, payout)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                bet_type=VALUES(bet_type),
                combination=VALUES(combination),
                payout=VALUES(payout)
        """
        cursor.execute(sql, (
            payout['race_id'],
            payout.get('bet_type'),
            payout.get('combination'),
            payout.get('payout')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_payout: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def insert_workout(workout):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO workouts (horse_id, race_id, date, course, distance, time, jockey, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                date=VALUES(date),
                course=VALUES(course),
                distance=VALUES(distance),
                time=VALUES(time),
                jockey=VALUES(jockey),
                notes=VALUES(notes)
        """
        cursor.execute(sql, (
            workout['horse_id'],
            workout['race_id'],
            workout['date'],
            workout.get('course'),
            workout.get('distance'),
            workout.get('time'),
            workout.get('jockey'),
            workout.get('notes')
        ))
        conn.commit()
    except Error as e:
        print(f"Error in insert_workout: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def update_track_condition_if_changed(race_id, new_condition):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 現在の値を取得
    cursor.execute("SELECT track_condition FROM races WHERE race_id=%s", (race_id,))
    row = cursor.fetchone()
    if row:
        current_condition = row[0]
        if current_condition != new_condition:
            cursor.execute(
                "UPDATE races SET track_condition=%s WHERE race_id=%s",
                (new_condition, race_id)
            )
            conn.commit()
            print(f"Updated race_id={race_id} track_condition: '{current_condition}' → '{new_condition}'")
        else:
            print(f"No change for race_id={race_id}: track_condition='{current_condition}'")
    else:
        print(f"Race not found: race_id={race_id}")

    cursor.close()
    conn.close()
