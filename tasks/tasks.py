from tasks import database

"""
Making functions for -
- getting the people in ## Done
- getting the people out ## Done

- assigning the people a hostel room ## Done
- issuing the people a fresh hostel room on spot ## Done
////
when the person has already registered for accommodation, 
- youll have his name on the portal, give him a room
- mark as in
- when leaving, mark as out
////
////
when the person needs to register for accommodation
- no name on the  in the list
- make him pay there
- query to make his accommodation in people to true and add his name to people_in_hostel
////


- taking the keys back from the people who are leaving
////
- check if the person is inside the hostel
- if yes directly mark him as out
////
"""


async def get_in(user_id: str):
    conn, cursor = database.make_db()
    """
    - Check if the person registered for the fest
    - Add that person to the people_in_campus table
    """
    # Checking the registration
    check_query = f"""
    select * from people where uid = '{user_id}'
    """
    cursor.execute(check_query)
    details = cursor.fetchall()
    if not details:
        print("GET IN: Not Registered")
        return {
            "message": "User not registered for the fest",
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "status": "Not Found",
        }
    print("GET IN: Registered")
    print(details)

    # Adding the person to the people_in_campus table after checking if the same tuple is already there
    check_query = f"""
    select * from people_in_campus where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if result :
        query = f"""
        update people_in_campus set campus = TRUE where uid = '{user_id}'
        """
        cursor.execute(query)
        conn.commit()
        print("GET IN: User already in the campus")
        return {
            "message": "User added to the people_in_campus table",
            "name": details[0][1],
            "email": details[0][2],
            "phone": details[0][3],
            "status": "INSIDE",
        }
    query = f"""
    insert into people_in_campus values ('{user_id}', TRUE)
    """
    cursor.execute(query)
    conn.commit()
    print("GET IN: User now in the campus")
    return {
        "message": "User added to the people_in_campus table",
        "name": details[0][1],
        "email": details[0][2],
        "phone": details[0][3],
        "status": "INSIDE",
    }


async def get_out(user_id: str):
    conn, cursor = database.make_db()
    """
    - Check if the person is in the campus
    - Remove that person from the people_in_campus table
    """
    # Checking if the person is in the campus
    check_query = f"""
    select * from people_in_campus where uid = '{user_id}'
    """
    cursor.execute(check_query)
    results = cursor.fetchall()
    if not results:
        print("GET OUT: Not Registered")
        return {
            "message": "User not in the campus",
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "status": "Not Found",
        }
    print("GET OUT: Registered")

    # Getting the details of the person
    query = f"""
    select * from people where uid = '{user_id}'
    """
    cursor.execute(query)
    details = cursor.fetchall()

    # Update the table people_in_campus to false in that row
    query = f"""
    update people_in_campus set campus = FALSE where uid = '{user_id}'
    """
    cursor.execute(query)
    conn.commit()
    return {
        "message": "User is Out of Campus",
        "name": details[0][1],
        "email": details[0][2],
        "phone": details[0][3],
        "status": "OUTSIDE",
    }


async def issue_hostel(user_id: str, room_no: str):
    conn, cursor = database.make_db()
    warning = "None"
    """
    - Check if the person is registered for the fest
        - if not then make him pay then and there
    - Check if the person is in the campus => loose check here
        - If he is not in campus make that true then and issue a warning
    - Issue a hostel room to the person
    """
    # checking registration for the fest
    query = f"""
    select * from people where uid = '{user_id}'
    """
    cursor.execute(query)
    result = cursor.fetchall()
    if not result:
        return {
            "message": "User not registered for the fest",
            "warning": "Not Found",
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
        }
    print("GIVE HOSTEL : User Registered")
    # getting details
    query = f"""
        select * from people where uid = '{user_id}'
        """
    cursor.execute(query)
    details = cursor.fetchall()

    # checking campus presence
    check_query = f"""
    select * from people_in_campus where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if not result:
        warning = "User was NOT in the campus"
        query = f"""
        insert into people_in_campus values ('{user_id}', TRUE)
        """
        cursor.execute(query)
        conn.commit()
        print(f"GIVE HOSTEL : {warning}")
    elif result[0][1] == False:
        warning = "User was NOT in the campus"
        query = f"""
        update people_in_campus set campus = TRUE where uid = '{user_id}'
        """
        cursor.execute(query)
        conn.commit()
        print(f"GIVE HOSTEL : {warning}")
    # check if the accomodation status is 'Yes', if not then return that the person did not opt for accomodaton
    check_query = f"""
    select uid, accomodation from people where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if result[0][1] == 'No':
        return {
            "message": "User did not opt for accomodation",
            "warning": "Not Found",
            "name": details[0][1],
            "email": details[0][2],
            "phone": details[0][3],
        }

    # issuing a hostel room
    # if the person is already in the hostel then update the room number
    check_query = f"""
    select * from people_in_hostel where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if result:
        query = f"""
        update people_in_hostel set hostel = TRUE, room = '{room_no}' where uid = '{user_id}'
        """
        cursor.execute(query)
        conn.commit()
        return {
            "message": "User has been issued a hostel room",
            "warning": warning,
            "name": details[0][1],
            "email": details[0][2],
            "phone": details[0][3],
            "room_no": room_no
        }

    query = f"""
    insert into people_in_hostel values ('{user_id}', TRUE, '{room_no}')
    """
    cursor.execute(query)
    conn.commit()

    return {
        "message": "User has been issued a hostel room",
        "warning": warning,
        "name": details[0][1],
        "email": details[0][2],
        "phone": details[0][3],
        "room_no": room_no
    }


async def hostel_on_spot(user_id: str, room_no: str):
    conn, cursor = database.make_db()
    """
    - Check if the person is registered for the fest
        - if not then make him pay then and there
    - Check if the person is in the campus => loose check here
        - If he is not in campus make that true then and issue a warning
    - Issue a hostel room to the person
    """
    warning = "None"
    # checking registration for the fest
    query = f"""
    select * from people where uid = '{user_id}'
    """
    cursor.execute(query)
    details = cursor.fetchall()
    if not details:
        return {
            "message": "User not registered for the fest",
            "warning": "Not Registered",
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
            "room_no": "Not Found"
        }

    # checking campus presence
    check_query = f"""
    select * from people_in_campus where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if not result:
        warning = "User was NOT in the campus"
        query = f"""
        insert into people_in_campus values ('{user_id}', TRUE)
        """
        cursor.execute(query)
        conn.commit()
    # update the presence in campus to true
    query = f"""
    update people_in_campus set campus = TRUE where uid = '{user_id}'
    """
    cursor.execute(query)
    conn.commit()

    # changing his/her accommodation status in the people table
    query = f"""
    update people set accomodation = 'Yes' where uid = '{user_id}'
    """
    cursor.execute(query)
    conn.commit()

    # issuing a hostel room
    # if the peron is already in the hostel then update the room number
    check_query = f"""
    select * from people_in_hostel where uid = '{user_id}'
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if result:
        query = f"""
        update people_in_hostel set hostel = TRUE, room = '{room_no}' where uid = '{user_id}'
        """
        cursor.execute(query)
        conn.commit()
        return {
            "message": "User has been issued a hostel room",
            "warning": warning,
            "name": details[0][1],
            "email": details[0][2],
            "phone": details[0][3],
        }
    query = f"""
    insert into people_in_hostel values ('{user_id}', TRUE, '{room_no}')
    """
    cursor.execute(query)
    conn.commit()
    return {
        "message": "User has been issued a hostel room",
        "warning": warning,
        "name": details[0][1],
        "email": details[0][2],
        "phone": details[0][3],
    }


async def take_keys(user_id: str):
    conn, cursor = database.make_db()
    check_query = f"""
    select * from people_in_campus where uid = '{user_id}' and campus = TRUE
    """
    cursor.execute(check_query)
    result = cursor.fetchall()
    if not result:
        return {
            "message": "User not in the campus",
            "name": "Not Found",
            "email": "Not Found",
            "phone": "Not Found",
        }
    query = f"""
    update people_in_campus set campus = FALSE where uid = '{user_id}'
    """
    cursor.execute(query)
    conn.commit()
    return {
        "message": "Keys Taken",
        "name": result[0][1],
        "email": result[0][2],
        "phone": result[0][3],
    }


"""
## Trivial Queries ##
- getting all the users inside the campus
- getting all the users inside the hostel
"""


async def get_all_in_campus():
    conn, cursor = database.make_db()
    query = f"""
    select people.uid ,people.name as name, people.email as email, people.phone as phone, people_in_campus.campus, people.accomodation as accommodation from people_in_campus inner join people on people_in_campus.uid = people.uid order by people_in_campus.campus desc
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result


async def get_all_in_hostel():
    conn, cursor = database.make_db()
    query = f"""
    select people.name as name, people.email as email, people.phone as phone, people_in_hostel.room as room_no, people_in_hostel.hostel from people_in_hostel inner join people on people_in_hostel.uid = people.uid where people_in_hostel.hostel = TRUE order by people_in_hostel.hostel desc 
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result


async def get_mismatch():
    conn, cursor = database.make_db()
    query = f"""
    select count(*) from (select * from (select * from people where accomodation='No') natural join (select * from people_in_campus where campus = TRUE)) 
    """
    cursor.execute(query)
    result = cursor.fetchall()
    return result
