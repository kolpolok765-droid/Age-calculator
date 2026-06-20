# Age Calculator App Specification

## Overview
The Age Calculator is a simple mobile or web application that allows users to calculate their exact age by selecting their birthdate from a calendar input. The app provides a clean, minimal interface with a light green and white theme.

---

## Core Features

### 1. Date of Birth Selection
- Users can select their birthdate using a calendar picker (date input UI).
- Input format: DD/MM/YYYY (or localized format depending on region).
- Prevent future date selection.

### 2. Age Calculation
The app calculates:
- Years
- Months
- Days

Example output:
- "You are 24 years, 5 months, and 12 days old."

### 3. Real-Time Calculation
- Age updates instantly when a valid date is selected.
- No need for a submit button (optional, can be included for web versions).

### 4. Reset Option
- A reset button clears the selected date and output.

---

## UI / UX Design

### Theme
- Primary Color: Light Green (#90EE90 or similar soft green)
- Background: White (#FFFFFF)
- Accent Color: Slightly darker green for buttons and highlights
- Text: Dark Gray (#333333)

### Layout
- Centered card layout
- Clean spacing with rounded corners
- Minimalist design

### Components
- Header: "Age Calculator"
- Date Picker Input (Calendar UI)
- Calculate/Auto-display result section
- Reset Button

---

## User Flow

1. User opens the app
2. User clicks on date input field
3. Calendar opens
4. User selects birthdate
5. App calculates age instantly
6. Result is displayed below input

---

## Edge Cases Handling

- If no date is selected → show placeholder text: "Please select your birthdate"
- If future date is selected → show error: "Birthdate cannot be in the future"
- Handle leap years correctly
- Handle timezone differences consistently

---

## Tech Stack (Suggested)

### Web App
- HTML5
- CSS3 (Flexbox/Grid)
- JavaScript (Date API or Moment.js / Day.js)

### Mobile App
- Flutter OR React Native

---

## Optional Enhancements

- Show countdown to next birthday
- Show zodiac sign based on birthdate
- Dark mode toggle (future update)
- Share result button
- Animated result display

---

## Accessibility

- Fully keyboard accessible
- Screen reader friendly labels
- High contrast support (optional enhancement)

---

## Future Improvements

- Multiple language support
- Save user profiles
- History of calculations
- PWA support for offline usage

---