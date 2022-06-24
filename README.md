
# InkBazaar.io
## Dylan Gnatz - dlg2178

InkBazaar is a tattoo appointment management platform
that provides an interface for artists and customers 
to manage appointments. Artists are able to upload their designs
and set their schedule, while customers can seek available designs in 
their area, and book appointments with local artists. 

## Database
My database for this project resides at "postgresql://dlg2178:<password>@35.196.192.139/proj1part2"

## ER Diagram
![ER Diagram](/final_ER.png?raw=true "ER Diagram")

## Description
The platform offers views for all of the entities. From the NavBar, users can view designs, artist lists, appointment lists, billing records, studio addresses, and customer profiles. 

The design view immediately renders all available designs, but search functionality has been implemented to allow users to filter by design ID, description, artist, or city.

The design view allows customers to book new appointments. Clicking the button to book any available design leads to a page where they can select a studio (filtered to be in the same city as the tattoo artist who made the design) and pick a time. Booking the appointment adds it to the appointment list and the user is redirected to the list of appointments.

Search functionality is also implemented on the artists view, to allow customers to search artists by id, name, or area. Clicking on artist's name links to their personal profile, which also shows all of their designs. 

Billing shows all the billing records for previous appointments and links to the appointment table. 

Studios lists the ids and addresses of all the studios in the system. 

Profile renders the customer's profile and details.

I have implemented the majority of the functionalities on the platform, but still need to implement user registration and authentication, which will separate the views and permissions between artists and customers. 

Also to be implemented is a form for artists to add new designs, as well as a billing module to generate new payments for appointments. 

## Interesting Database Interactions

### Search Functions
My implementation of search on designs and artists required interesting database operations, as I wanted to scan over multiple fields and allow search for partial terms. As such, I had to make creative creative use of the wildcard character '%' and LIKE clauses to make the search robust. Example: 

"SELECT designs.design_id, artists.name, designs.description, artists.city, artists.state, designs.cost, designs.available, artists.artist_id FROM designs JOIN artists ON designs.artist_id = artists.artist_id WHERE designs.design_id = '{}' OR artists.name LIKE '%%{}%%' OR designs.description LIKE '%%{}%%' OR artists.city LIKE '%%{}%%';".format(intterm, searchterm, searchterm, searchterm)"

### Appointments table 
The appointments table is another interesting page as it required the use of multiple left joins to get all the data that needed to be displayed. The query required the joining of 6 different tables, as you can see here:

"SELECT appointments.appointment_id, customers.name, artists.name, designs.description, appointments.start_time, appointments.end_time, appointments.projected_cost, studio.address, payments.amount, artists.artist_id, customers.customer_id, designs.design_id, studio.studio_id, payments.payment_id FROM appointments LEFT JOIN customers ON appointments.customer_id = customers.customer_id LEFT JOIN artists ON appointments.artist_id = artists.artist_id LEFT JOIN designs ON appointments.design_id = designs.design_id LEFT JOIN studio ON appointments.studio_id = studio.studio_id LEFT JOIN payments ON appointments.payment_id = payments.payment_id;"


