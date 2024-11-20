
# Online Auction System with Binomial Heap-Based Bidding  

## About the Project  
The **Online Auction System with Binomial Heap-Based Bidding** is a web application built using Python and the Django framework. This platform enables efficient and user-friendly auction management for both buyers and sellers. 

## Key Features  
1. **User Registration and Authentication**:  
   - Secure user account creation, login, and profile management.  

2. **Auction Creation**:  
   - Sellers can list items for auction by providing item details, starting prices, and auction durations.  

3. **Efficient Bidding Process**:  
   - Buyers can place bids on active auctions.  
   - The **Binomial Heap** ensures efficient tracking of the highest bid and the associated bidder.  

4. **Real-Time Bid Status Tracking**:  
   - Users can monitor the status of ongoing auctions and their bids.  

5. **Automatic Auction Closure**:  
   - Auctions close automatically when the specified duration expires, and the highest bidder is declared the winner.  

6. **Interactive User Interface**:  
   - Users can view active bids, won auctions, and detailed auction information.  
 

## Technical Specifications  
 

### **Software Requirements**:  
1. **Programming Language**: Python  
2. **Framework**: Django  
3. **Database**: MySQL  
4. **Frontend Technologies**:  
   - HTML, CSS, and JavaScript  
5. **Additional Libraries**:  
   - Django ORM for database operations  
   - Pickle for serialization  

### **Hardware Requirements**:  
1. **Processor**: Intel Core 2 Duo or higher  
2. **RAM**: Minimum 3 GB  
3. **Hard Disk Space**: Minimum 2 GB  

## Installation and Setup  

### Prerequisites:  
1. Install Python (3.x or higher).  
2. Install MySQL.  
3. Install Django using pip:  
   ```bash  
   pip install django  
   ```  

### Steps to Run the Project:  
1. Clone the repository to your local machine.  
   ```bash  
   git clone <repository_url>  
   ```  

2. Navigate to the project directory.  
   ```bash  
   cd online_auction  
   ```  

3. Apply database migrations.  
   ```bash  
   python manage.py makemigrations  
   python manage.py migrate  
   ```  

4. Start the development server.  
   ```bash  
   python manage.py runserver  
   ```  

5. Open your browser and navigate to localhost.  



  
