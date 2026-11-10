export function getCurrentTimeInTimeZone(timeZone: string) {
    const options: Intl.DateTimeFormatOptions = {
        timeZone,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false
    };

    const formatter = new Intl.DateTimeFormat('en-CA', options);
    return formatter.format(new Date());
}

export function check_appointment_availability(datetime: string): string {
    console.log("Checking appointment availability:", datetime);

    return JSON.stringify(
        {
            success: true,
            available: true,
            datetime,
            message: "The requested appointment slot is available."
        }
    )
}

export function schedule_appointment(
    datetime: string,
    name: string,
    email: string
): string {
    console.log("Scheduling appointment:");
    console.log({ datetime, name, email });

    return JSON.stringify({
        success: true,
        appointment: { datetime, name, email },
        message: "Appointment scheduled successfully."
    });
}

export function delete_appointment(
    datetime: string,
    name: string,
    email: string
): string {
    console.log("Deleting appointment:");
    console.log({ datetime, name, email });

    return JSON.stringify({
        success: true,
        appointment: { datetime, name, email },
        message: "Appointment deleted successfully."
    });
}
