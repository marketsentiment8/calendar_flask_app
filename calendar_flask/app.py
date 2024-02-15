from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Configuration
app.config['DEBUG'] = True

# Define a list to store events
initial_events = []

# Function to parse events from log.txt and format them for FullCalendar
def parse_events_from_log():
    with open('log.txt', 'r') as log_file:
        lines = log_file.readlines()

    for line in lines:
        parts = line.strip().split(', ')
        if len(parts) == 3:
            title = parts[0].replace('Form submission - Title: ', '')
            start = parts[1].replace('Start: ', '')
            end = parts[2].replace('End: ', '')
            initial_events.append({
                'title': title,
                'start': start,
                'end': end
            })

parse_events_from_log()  # Load initial events from log.txt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_events')
def get_events():
    # Return your events, replace this with your event data
    return jsonify(initial_events)

@app.route('/add_event', methods=['POST'])
def add_event():
    title = request.form.get('title')
    start = request.form.get('start')
    end = request.form.get('end')

    if title and start and end:
        new_event = {
            'title': title,
            'start': start,
            'end': end
        }
        initial_events.append(new_event)

        # Save the event to the log.txt file (appending mode)
        log_data = f"Form submission - Title: {title}, Start: {start}, End: {end}\n"
        with open('log.txt', 'a') as log_file:
            log_file.write(log_data)

        return jsonify({'message': 'Event added successfully'})

    return redirect(url_for('index'))

@app.route('/edit_event', methods=['POST'])
def edit_event():
    title = request.form.get('title')
    start = request.form.get('start')
    end = request.form.get('end')

    if title and start and end:
        event_to_edit = {
            'title': title,
            'start': start,
            'end': end
        }

        # Open the log.txt file in read mode and read its lines
        with open('log.txt', 'r') as log_file:
            lines = log_file.readlines()

        # Open the log.txt file in write mode to update it
        with open('log.txt', 'w') as log_file:
            for line in lines:
                # Check if the line contains the old event data and replace it with the new event data
                if (f'Title: {title}' in line and
                    f'Start: {start}' in line and
                    f'End: {end}' in line):
                    updated_line = f'Title: {title}, Start: {start}, End: {end}\n'
                    log_file.write(updated_line)
                else:
                    log_file.write(line)

        return jsonify({'message': 'Event edited successfully'})

    # Handle invalid request or errors
    return jsonify({'message': 'Invalid request or error'})

@app.route('/remove_event', methods=['POST'])
def remove_event():
    title = request.form.get('title')
    start = request.form.get('start')
    end = request.form.get('end')

    if title and start and end:
        event_to_remove = {
            'title': title,
            'start': start,
            'end': end
        }

        for event in initial_events:
            if event == event_to_remove:
                initial_events.remove(event)

        # Remove the event from the log.txt file
        with open('log.txt', 'r') as log_file:
            lines = log_file.readlines()

        with open('log.txt', 'w') as log_file:
            for line in lines:
                if (f'Title: {title}' in line and
                    f'Start: {start}' in line and
                    f'End: {end}' in line):
                    continue  # Skip the line to remove
                log_file.write(line)

        return jsonify({'message': 'Event removed successfully'})

    return jsonify({'message': 'Invalid request'})

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
