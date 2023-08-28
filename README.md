
# Tony CMS

#### Video Demo: <>

#### Description: 
Hello CS50! Allow me to introduce my dynamic web application, designed to enhance the customer-staff relationships for businesses. 
Initially, I had planned to create a basic website for a fictitious business. However, I pivoted towards constructing a comprehensive 
content management system (CMS) that provides businesses with seamless tools for managing their customer interactions.

The foundation of my web application lies in Django, Python, HTML, CSS, and a touch of Javascript. The intricate database operations 
are adeptly supported by PostgreSQL via PgAdmin.

Foregoing the task of fabricating a custom authentication system, I opted for Django's trusted authentication mechanism, 
ensuring top-notch security. This integration entailed the creation of three pivotal functions: 'login' (secure sign-in), 
'register' (new user registration), and 'logout' (account sign-out), all nestled within 'log.py'.

Subsequent to successfully establishing the user registration feature, I directed my focus towards data storage 
feature named "My Files." This module empowers users to upload and securely store PDF documents in the database. 
Central to this feature is the Python function 'pdf_registry', which handles HTML requests, ensuring files are associated 
with the appropriate user profiles. Moreover, I've incorporated a straightforward checkbox, allowing usersto delete files 
from their accounts.

Transitioning to the 'Appointments' feature, I've constructed three Python functions. 'View Current Appointments' showcases 
upcoming engagements in a table, complete with a checkbox enabling users to cancel any scheduled appointments. 'Make New Appointments' 
is fashioned as an intuitive form, awaiting user input, which, upon completion, populating the database. Meanwhile, 
'View Past Appointments', exclusively curated for administrators, archives completed or cancelled meetings, granting admins the 
option to restore any displayed appointment.

To further enhance engagement, I created a chat feature, fostering seamless interactions between Admins (staff members) and regular users. 
This functionality is constructed by six Python fucntions, each responsible for distinct tasks like 'admin_chat', regular user chat, 
data acquisition, chat removal, message relaying, and file transmission. I've separated the admin and regular user chat modules 
(and their respective HTML structures) to reinforce security, optimize management, and refine implementation. Both chat variants 
utilize the data acquisition and chat removal functions. Furthermore, a specialized function oversees the 'send' button, channeling 
chat content to the database. Complementing this, I've instated a file-sharing mechanism, allowing users to append files in chats 
and optionally save them in "My Files."

Furthermore, leveraging online templates, I crafted the front-end using HTML, CSS, and Javascript to ensure a user-friendly and 
responsive interface.

While the project may currently be in its infancy and still evolving, the journey of codingand feature integration has been incredibly rewarding. 
I'm confident that this is just the beginning of an exciting and transformative venture.
