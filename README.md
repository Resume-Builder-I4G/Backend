# Backend ⚡🔥

[Link to API](https://resume-builder-i4g.herokuapp.com)

## Endpoints 🚀🔥

### Home
    / -- GET
        Request:
            body: -- null
            headers: no additional header
        Response:
            Redirects to the docs page(Official docs still in progress)

### Auth
    /auth/signup  -- POST
        Request:
            JSON body:
                    name: string
                    email: string
                    password: string
        Response: JSON
            If email exist:
                error: string
                message: string
                status code: 400
            if email doesn't exist:
                user details, status code:200
        You receive a welcome mail
    /auth/signin -- POST
        Request:
            JSON body:
            email: string
            password: string
        Response: JSON
            token(add this to request headers for other request as headers['Authorization']='Bearer <token>' for authN
            user details
            if email is not registered:
                error: string
                message: string
                status code:400
    /get_password_token -- POST
        Request:
            JSON body:
                email: string
            Headers:
                Authorization must not be present
        Response: JSON
            message: string
            user 
            You receive a mail telling you how to reset your password
    /reset_password/<token>   -- POST
        link is sent to mail
        Request:
            JSON body:
                password: string
                confirm password: string
            Headers:
                    Authorization must not be present
        Response:
            user

### Users
    /users -- GET (Endpoint will be removed soon😪, was used for testing)
        Request:
            No request body, no additional request headers
        Response:
            body: JSON array of users
            status code:200
    /user -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            body: JSON data, contains achievements, hobbies, languages, certificates, education, work experience arrays respectively.
            status code:200
    /user -- PUT
        Request:
            Headers: Authorization='Bearer <token>'
            Form: 
                Data to update
            File: profile picture of the user
                avatar: file storage(image type) if not image type returns a 400 status code
        Response:
            body:
                JSON data of the user, avatar has been saved to server and the url to the image is returned
    /confirm -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            body: none
        Response:
            user

### Skills
    /skills -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Skills of the user with user_id in it or empty array if has not added any skill
    /skills -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body:
                name: string(If name exist returns a 400 status code)
                level: integer
        Response:
            status code: 201
            body:
                name: string
                level: integer
                _id: string(uuid)
                user_id: string(uuid)    
    /skills/<id> -- PUT
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body: at least one of the two must be given
                name: string(If name exist returns a 400 status code)
                level: integer
        Response:
            status code: 201
            body:
                name: string
                level: integer
                _id: string(uuid)
                user_id: string(uuid) 
    /skills/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204

### Languages
        /languages -- GET
            Request:
                Headers: Authorization='Bearer <token>'
                Body: No body
            Response:
                Languages of the user with user_id in it or empty array if user has not added any language
        /languages -- POST
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body:
                    name: string(If name exist returns a 400 status code)
                    proficiency: string
            Response:
                status code: 201
                body:
                    name: string
                    proficiency: string
                    _id: string(uuid)
                    user_id: string(uuid)   
        /languages/<id> -- PUT
            If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    name: string(If name exist returns a 400 status code)
                    proficiency: string
            Response:
                status code: 201
                body:
                    name: string
                    proficiency: string
                    _id: string(uuid)
                    user_id: string(uuid) 
        /languages/<id> -- DELETE
            If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
            Response:
                status code: 204

### Certificates
    /certificates -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Certificates of the user with user_id in it or empty array if has not added any certificate
    /certificates -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body:
                name: name of certification, string(If name exist returns a 400 status code)
                whatever you put again🤧
        Response:
            status code: 201
            body:
                name: string
                any other thing passed
                _id: string(uuid)
                user_id: string(uuid)   
    /certificates/<id> -- PUT
        If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    name: string(If name exist returns a 400 status code)
                    other things you want to add
            Response:
                status code: 201
                body:
                    name: string
                    others
                    _id: string(uuid)
                    user_id: string(uuid)
            whatever you want to change
    /certificates/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204

### Hobbies
    /hobby -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Hobbies of the user with user_id in it or empty array if has not added any hobby
    /hobby -- POST
        Request:
                Headers: Authorization='Bearer <token>'
                JSON body:
                    name: string(If name exist returns a 400 status code)
        Response:
            status code: 201
            body:
                name: string
                _id: string(uuid)
                user_id: string(uuid)   
    /hobby/<id> -- PUT
        If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    name: string(If name exist returns a 400 status code)
            Response:
                status code: 201
                body:
                    name: string
                    _id: string(uuid)
                    user_id: string(uuid)
    /hobby/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204

### Work Experience
    /experiences -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Work Experience of the user with user_id in it or empty array if has not added any work experience
    /experiences -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body:
                title: string
                company: string
                start_date: datetime
                end_date(if None then saved as Present): datetime or None
                description(can be none): string
        Response:
            status code: 201
            body:
                title: string
                company: string
                start_date: datetime
                end_date(if None then saved as Present): datetime or None
                description(can be none): string
                _id: string(uuid)
                user_id: string(uuid)   
    /experiences/<id> -- PUT
        If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    whatever you want to change
            Response:
                status code: 201
                body:
                    updated data
                    proficiency: string
                    _id: string(uuid)
                    user_id: string(uuid)
    /experiences/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204

### Education
    /education -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Education of the user with user_id in it or empty array if has not added any education
    /education -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body:
                course: string
                school: string
                start_date: datetime
                end_date(if None then saved as Present): datetime or None
                description(can be none): string
        Response:
            status code: 201
            body:
                course: string
                school: string
                start_date: datetime
                end_date(if None then saved as Present): datetime or None
                description(can be none): string
                _id: string(uuid)
                user_id: string(uuid)  
    /education/<id> -- PUT
        If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    whatever you want to change
            Response:
                status code: 201
                body:
                    updated data
                    proficiency: string
                    _id: string(uuid)
                    user_id: string(uuid)
    /education/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204

### Achievements
    /achievements -- GET
        Request:
            Headers: Authorization='Bearer <token>'
            Body: No body
        Response:
            Achievement of the user with user_id in it or empty array if has not added any achievement
    /achievements -- POST
        Request:
            Headers: Authorization='Bearer <token>'
            JSON body:
                Don't know what will be needed in the client side, hence anything can be passed 🤧
    /achievements/<id> -- PUT
        If id doesn't exist returns a 404 error
            Request:
                Headers: Authorization='Bearer <token>'
                JSON body: at least one of the two must be given
                    whatever you want to change
            Response:
                status code: 201
                body:
                    updated data
                    proficiency: string
                    _id: string(uuid)
                    user_id: string(uuid) 
    /achievements/<id> -- DELETE
        If id doesn't exist returns a 404 error
        Request:
            Headers: Authorization='Bearer <token>'
        Response:
            status code: 204