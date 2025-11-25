
var selectedEvent = null;

//     ####   ###   #   #  ####    ###   #   #  #####  #   #  #####   ####
//    #      #   #  ## ##  #   #  #   #  ##  #  #      ##  #    #    #
//    #      #   #  # # #  ####   #   #  # # #  ####   # # #    #     ###
//    #      #   #  #   #  #      #   #  #  ##  #      #  ##    #        #
//     ####   ###   #   #  #       ###   #   #  #####  #   #    #    ####

        const Announcements = {
            components: {

            },
            setup(props, { emit }) {
                const items = ref([

                ])
                return {
                  items
                }
            },
            template: document.getElementById('Announcements')
        } 
        const Filters = {
            components: {

            },
            props: {
              filterChange: {
                type: Function
              }
            },
            setup(props, { emit }) {
              const dateRange = ref([])
              watch (dateRange, (nv) => {
                props.filterChange(nv)
              })
              return {
                  dateRange
              }
            },
            template: document.getElementById('Filters')
        }
        const EventDialog = {
            components: {
            },
            props: {
              event: {
                type: Object
              }
            },
            setup(props, { emit }) {
              const dialogVisible = ref(false)

              return {
                dialogVisible,
              }
            },
            template: document.getElementById('EventDialog')
        }            
        const EventCard = {
            components: {
              EventDialog
            },
            props: {
              event: {
                type: Object
              },
              seeAll: {
                type: Function
              }
            },
            setup(props, { emit }) {
              const setEvent = () => {
                selectedEvent = props.event
              }
                return {
                  setEvent,
                }
            },
            template: document.getElementById('EventCard')
        }    

        const EventGrid = {
            components: {
              EventCard
            },
            props: {
              events: {
                type: Array
              },
              seeAll: {
                type: Function
              }
            },
            setup(props, { emit }) {
            },
            template: document.getElementById('EventGrid')
        }    

//    ####     #     ####  #####   ####
//    #   #   # #   #      #      #
//    ####   #####  #  ##  ####    ###
//    #      #   #  #   #  #          #
//    #      #   #   ####  #####  ####

        const MainBase = {
            components: {
              Announcements,
              Filters,
              EventGrid,
              EventDialog,


            },
            setup(props, { emit }) {
              const eventList = [
                {
                  "image": "images/resim1.jpg",
                  "alt": "ÖST 2024 Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-03",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim2.jpg",
                  "alt": "Forest Park Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-07",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim3.jpg",
                  "alt": "Go! Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-10",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim3.jpg",
                  "alt": "Forest Park Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-13",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim2.jpg",
                  "alt": "Go! Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-16",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim1.jpg",
                  "alt": "ÖST 2024 Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-18",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim1.jpg",
                  "alt": "Forest Park Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-20",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim2.jpg",
                  "alt": "Go! Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-22",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim3.jpg",
                  "alt": "ÖST 2024 Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-25",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim3.jpg",
                  "alt": "Forest Park Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-27",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim2.jpg",
                  "alt": "Go! Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-29",
                  "see_all_link": "#"
                },
                {
                  "image": "images/resim1.jpg",
                  "alt": "ÖST 2024 Poster",
                  "event_name": "Event Name",
                  "community_name": "Community Name",
                  "location": "LocationLocation...",
                  "time": "00:00",
                  "date": "2025-11-30",
                  "see_all_link": "#"
                }
              ]              
              const events = ref(
                eventList
              )
              const selEvent = ref(null)
              const dialogVisible = ref(false)

              const seeAll = (val) => {
                selEvent.value = selectedEvent;
                
                dialogVisible.value = true;
              }

              const onFilterChange = (val) => {
                if (!val) {
                  events.value = eventList;
                } else {
                  let startDate = moment(val[0]).format("YYYY-MM-DD")
                  let endDate = moment(val[1]).format("YYYY-MM-DD")
                  let newList = eventList.filter(item => {
                    return item.date >= startDate && item.date <= endDate
                  })
                  events.value = newList;
                }
              }
                return {
                  events,
                  onFilterChange,
                  seeAll,
                  dialogVisible,
                  selEvent,
                }
            },
            template: document.getElementById('MainBase')
        }    

