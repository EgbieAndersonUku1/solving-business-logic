# Scenario: Event Management System

## Business Context:

You are building an event management system for a company that organises various events, such as conferences, workshops, and seminars. The company needs a way to manage events, attendees, and the different roles that attendees can have within an event.

## Requirements:

### Events

Each event has a title, date, location, and description. An event can have multiple attendees. Each event can have multiple sessions, such as keynote speeches, workshops, and panel discussions.

### Attendees

Each attendee has a first name, last name, email, and phone number. Attendees can attend multiple events. An attendee can have a specific role in an event, such as "Speaker," "Volunteer," or "Attendee."

### Roles

Roles define the function of an attendee within an event. Some roles are predefined: "Speaker," "Volunteer," "Organizer," and "Attendee." An attendee can have different roles in different events (e.g., an attendee can be a "Speaker" in one event and a "Volunteer" in another).

### Sessions

Each session belongs to a specific event. Sessions have a title, start time, end time, and a description. A session can have one or more speakers (attendees with the role of "Speaker").
