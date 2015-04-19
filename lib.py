import copy

def save_user_and_index(db_handler, es_handler, user_model):
    
    db_handler.session.add(user_model)
    db_handler.session.commit()
    
    user_model.id
    
    doc_to_index = copy.copy(user_model.__dict__)
    if '_sa_instance_state' in doc_to_index:
        del doc_to_index['_sa_instance_state']
    
    print doc_to_index
    
    es_handler.index(index="github_user",
                    doc_type="user_doc",
                    body=doc_to_index,
                    timeout=30)

def save_project_and_index(db_handler, es_handler, project_model):
    
    db_handler.session.add(project_model)
    db_handler.session.commit()
    
    project_model.id
    
    doc_to_index = copy.copy(project_model.__dict__)
    if '_sa_instance_state' in doc_to_index:
        del doc_to_index['_sa_instance_state']
    
    print doc_to_index
    
    es_handler.index(index="github_project",
                    doc_type="project_doc",
                    body=doc_to_index,
                    timeout=30)

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import random
    import string

    db.drop_all()
    db.create_all()

    first_names = [
        'Harry', 'Amelia', 'Oliver', 'Jack', 'Isabella', 'Charlie','Sophie', 'Mia',
        'Jacob', 'Thomas', 'Emily', 'Lily', 'Ava', 'Isla', 'Alfie', 'Olivia', 'Jessica',
        'Riley', 'William', 'James', 'Geoffrey', 'Lisa', 'Benjamin', 'Stacey', 'Lucy'
    ]
    last_names = [
        'Brown', 'Smith', 'Patel', 'Jones', 'Williams', 'Johnson', 'Taylor', 'Thomas',
        'Roberts', 'Khan', 'Lewis', 'Jackson', 'Clarke', 'James', 'Phillips', 'Wilson',
        'Ali', 'Mason', 'Mitchell', 'Rose', 'Davis', 'Davies', 'Rodriguez', 'Cox', 'Alexander'
    ]
    locations = [
        ("Shanghai", "China"),
        ("Istanbul", "Turkey"),
        ("Karachi", "Pakistan"),
        ("Mumbai", "India"),
        ("Moscow", "Russia"),
        ("Sao Paulo", "Brazil"),
        ("Beijing", "China"),
        ("Tianjin", "China"),
        ("Guangzhou", "China"),
        ("Delhi", "India"),
        ("Seoul", "South Korea"),
        ("Shenzhen", "China"),
        ("Jakarta", "Indonesia"),
        ("Tokyo", "Japan"),
        ("Mexico City", "Mexico"),
        ("Kinshasa", "Democratic Republic of the Congo"),
        ("Bangalore", "India"),
        ("New York City", "United States"),
        ("London", "United Kingdom"),
        ("Bangkok", "Thailand"),
        ("Tehran", "Iran"),
        ("Dongguan", "China"),
        ("Lagos", "Nigeria"),
        ("Lima", "Peru"),
        ("Ho Chi Minh City", "Vietnam"),
        ]

    for i in range(len(first_names)):
        user = User()
        user.first_name = first_names[i]
        user.last_name = last_names[i]
        user.email = user.first_name.lower() + "@example.com"
        tmp = ''.join(random.choice(string.digits) for i in range(10))
        user.phone = "(" + tmp[0:3] + ") " + tmp[3:6] + " " + tmp[6::]
        user.city = locations[i][0]
        user.country = locations[i][1]
        db.session.add(user)

    images = ["Buffalo", "Elephant", "Leopard", "Lion", "Rhino"]
    for name in images:
        image = Image()
        image.name = name
        image.path = name.lower() + ".jpg"
        db.session.add(image)

    for i in [1, 2, 3]:
        file = File()
        file.name = "Example " + str(i)
        file.path = "example_" + str(i) + ".pdf"
        db.session.add(file)

    db.session.commit()
    return