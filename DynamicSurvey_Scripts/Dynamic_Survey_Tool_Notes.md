Dynamic Survey Tool Project:
Data Cleaning and Visualization

Deliverables: 
    1. Cleaned Spreadsheets
        - one for each run
        - include states as ints to make easier for ML
    2. Visualizations (by time)
        - PD and MR gamma measurements (also by depth)
        - drilling state machine (ROP, WOB, Depth)

Data Fields
    - MR_Flow.M: 1/0 entries; used for validating pumps on or off
    - MR_Gama.5S5A: measurements of gamma (higher up on the string)
    - MR_ROTATION: 1/0 entries; used to validate if rotating
    - MR_RPM-AVG.MR: rotations per minute (of the bit)
    - MR_VIBA: axial vibration
    - MR_VIBL: lateral vibration
    - PD_Axial Vibration: axial vibration at pulser
    - PD_Gamma: measurements of gamma at the pulser
    - PD_Lateral Vibration: lateral vibration at pulser
    - PD_Pump_Event: entries are strings "Pumps On Event"/"Pumps Off Event"; used for validating pumps on/off
    - RT_Depth: real time depth (feet)
    - RT_Pumps_Off: flow rate (gallons/minute)
    - RT_Pumps_On: flow rate (gallons/minute)
    - RT_ROP: rate of penetration; speed of drilling (ft/hr)
    - RT_RPM.W: rotations per minute (of the bit)
    - RT_SLIDE_BIT: 1/0 entries; used for validating sliding drilling
    - RT_Time: timestamp
    - RT_WOB: weight on bit (thousands of pounds)

Drilling State Machine (codings and classification criteria)
    0: Pumps Off 
        No activity is occurring
        Flow = Low
        Rotation = Low
        Vibration = 0

    1: Pumps On
        Fluid is moving past the tool. We are getting ready to drill
        Flow = High
        Rotation = Low
        Vibration = Near 0
    2: Sliding Drilling
        Building up angle downhole to change direction of drilling
        Flow = High
        Rotation = Low
        Vibration = High
    3: Rotating
        The drill bit is rotating and ready for rotational drilling
        Flow = High
        Rotation = High
        Vibration = High
    4: Rotating Drilling
        Traditional drilling
        Flow = High
        Rotation = High
        Vibration = High

Nota Bene
    - a section of pipe is 90 feet
    - PD refers to the pulser, which is downhole
    - MR (motor?) also refers to downhole, but higher than the pulser

Plan of Action
    1. Data Cleaning & Preprocessing:
        A. Rig Spreadsheets to Dataframes 
            -  Make rig spreadsheets into pandas Dataframes for easy manipulation and preservation of original spreadsheets
            -  Get rid of extraneous columns: 
                ["RT_TVD", "RT_ACTIVITY", "RT_Botm", "RT_SLIDE", 
                "MR_INC.M", "MR_LINC.M", "MR_AZM.M", "MR_LAZM.MR", "MR_DIPA.M", "MR_MAGF.M", "MR_TEMP.M", "MR_VIBT.MR",
                "PD_Temperature", "PD_X Vibration", "PD_Y Vibration"]
            -  Remove rows that do not include depth measurements
            -  Remove rows that have no data in them (except depth measurements)
        B. Run Dataframes
            - create a dataframe for each run from the rig dataframe using the rows that are within the start/end dates and are closest with the given start/end depths
        C. Transformed Run Dataframes
            - calculate flow, rotation, and vibration and create new dataframe with these inputs as well as drilling state machine estimation
            - for flow, rotation, and vibration:
                * if one entry in possible fields, use that entry
                * if multiple entries across possible fields, use average of those entries
                * if no entry in possible fields, use last calculation
            - Possible Fields for Calculations
                * Flow: RT_Pumps_Off, RT_Pumps_On
                * Rotation: MR_RPM-AVG.MR, RT_RPM.W
                * Vibration: MR_VIBA, MR_VIBL, PD_Axial Vibration, PD_Lateral Vibration
            - include MR_Gama.5S5A and PD_Gamma, but do not change any data entries (there will be blank cells)
            - include RT_ROP and RT_WOB; copy last entry into current cell if empty
            - calculate drilling state machine code based on classification criteria listed above
        D. Validating Run Dataframes
            - create dataframes from original run dataframes with the following fields:
                RT_SLIDE_BIT, MR_FLOW.M, MR_ROTATION, PD_Pumps_Event
                * convert strings in PD_Pumps_Event to 1/0 

1. **Load and Explore Data:**  
   - Use `pandas` to read and inspect the spreadsheet  
   - Identify missing values and inconsistencies  

2. **Preprocess Data:**  
   - Convert timestamps to datetime format (`pd.to_datetime`)  
   - Sort by timestamp  
   - Handle missing or noisy data  
   - Merge or clean rows where necessary  
   - Filter by depth range  

3. **Classify Drilling States:**  
   - Use logical conditions to define each state  
   - Create a new column to label the state at each timestamp  

4. **Visualize Data:**  
   - Use `matplotlib` and `plotly` for interactive time series plots  
   - Create a zoomable drilling state graph  
   - Generate a separate Gamma comparison plot  

5. **Export Cleaned Data:**  
   - Save processed data to a new Excel or CSV file for further analysis  

---

### **Recommended Python Libraries**  
- **Data Handling:** `pandas`, `numpy`  
- **Visualization:** `matplotlib`, `plotly`, `seaborn`  
- **Interactive Exploration:** `plotly.express`, `dash` (optional for dashboards)  

---

### **Best Practices for Data Analysis**  
- **Understand the Domain:** Talk to industry experts or study oil drilling processes  
- **Use Efficient Data Structures:** If handling large data, optimize with `dask` or `numpy`  
- **Handle Time Series Properly:** Ensure consistent timestamps and avoid gaps  
- **Document Assumptions:** Keep track of criteria used for state classification  
- **Validate Results:** Compare derived states against known drilling logs or expert input  
