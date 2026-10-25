import { useEffect, useMemo, useState } from 'react'
import { divIcon, latLng } from 'leaflet'
import { MapContainer, Marker, Popup, TileLayer, useMap } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import './MapPage.css'

export type HousingCategory = 'Single Rooms' | 'Bedsitter' | '1-Bedroom' | '2-Bedroom' | '3-Bedroom'
export interface HousingListing {
  id: string
  name: string
  category: HousingCategory | 'Off-Campus Hostels' | 'Main Anchor'
  price?: { min: number; max: number }
  distance?: string
  travelTime?: string
  coordinates: [number, number]
  location?: string
  features?: string[]
}

export const CAMPUS: HousingListing = { id: 'daystar-campus', name: 'Daystar Main Campus Gate', category: 'Main Anchor', coordinates: [-1.4525, 36.964], location: 'Athi River Campus' }
export const HOUSING: HousingListing[] = [
  { id: 'kryptons-apt', name: 'Kryptons Apartments', category: 'Bedsitter', price: { min: 6000, max: 8000 }, distance: '570 m', travelTime: '5–7 mins walk', coordinates: [-1.4532, 36.9654], location: 'H26V+P45, Athi River', features: ['Private balcony', 'Granite-top kitchenette', 'Ensuite bathroom with hot water', 'Perimeter electric fence', 'High-capacity water storage'] },
  { id: 'daystar-hostels-heri', name: 'Daystar Hostels (Heri Homes Ltd)', category: 'Single Rooms', price: { min: 5000, max: 7500 }, distance: '575 m', travelTime: '5–7 mins walk', coordinates: [-1.453, 36.965], location: 'H26V+2F8, Athi River', features: ['Single and double occupancy rooms', 'Study desks & wardrobes', 'High-speed Wi-Fi', 'Communal study lounges', 'Biometric security'] },
  { id: 'orange-county', name: 'Orange County (OC) Hostels', category: 'Bedsitter', price: { min: 5500, max: 7500 }, distance: '600 m', travelTime: '6–8 mins walk', coordinates: [-1.4535, 36.966], location: 'H26V+9F5, Athi River', features: ['Self-contained rooms', '24/7 access', 'Reliable water backup', 'Ground-floor convenience stores'] },
  { id: 'daystar-apts-kinanie', name: 'Daystar Apartments (Kinanie Road)', category: '1-Bedroom', price: { min: 10000, max: 14000 }, distance: '690 m', travelTime: '8–10 mins walk', coordinates: [-1.455, 36.968], location: 'H25V+4X3, Kinanie, Athi River', features: ['Separate living room', 'Fitted wardrobes', 'Balcony overlooking Lukenya Hills', 'Cabro parking', 'Borehole water'] },
  { id: 'keris-hostels', name: 'Keris Hostels', category: 'Single Rooms', price: { min: 4500, max: 6500 }, distance: '750 m', travelTime: '9–11 mins walk', coordinates: [-1.456, 36.969], location: 'H26V+VR2, Athi River', features: ['Affordable studio layout', 'Quiet study environment', 'Secure gate access', 'Consistent water availability'] },
  { id: 'luminar-hostel', name: 'Luminar Hostel', category: 'Single Rooms', price: { min: 4500, max: 6500 }, distance: '980 m', travelTime: '12–15 mins walk', coordinates: [-1.458, 36.971], location: 'Lukenya campus zone', features: ['Compact private hostel', 'Shared common spaces', 'Near university boundary'] },
  { id: 'mti-hostels', name: 'M.T.I Hostels Athi River', category: 'Off-Campus Hostels', price: { min: 5000, max: 7000 }, distance: '5.9 km', travelTime: '10–12 mins drive', coordinates: [-1.448, 36.982], location: 'Athi River Township, HX3P+WF4', features: ['Student hostel facility', '24/7 access control', 'Close to public transit'] },
  { id: 'sunset-boulevard', name: 'Sunset Boulevard Apartments', category: '3-Bedroom', price: { min: 16000, max: 35000 }, distance: '6.2 km', travelTime: '10–12 mins drive', coordinates: [-1.445, 36.985], location: '39 Quarry Road, Athi River Town', features: ['Gated estate', '1, 2 and 3 bedroom configurations', '24/7 security patrol', 'On-site commercial centre', 'Laundry yards and cabro driveways'] },
  { id: 'vision-four', name: 'Vision Four Apartments', category: '2-Bedroom', price: { min: 22000, max: 28000 }, distance: '6.7 km', travelTime: '12–15 mins drive', coordinates: [-1.442, 36.989], location: 'Site Road, near To Glory Shop, Athi River', features: ['24-hour gated access', 'Spacious master ensuite', 'Ideal for staff and long-term tenants'] },
]

const filters = ['All', 'Single Rooms', 'Bedsitter', '1-Bedroom', '2-Bedroom', '3-Bedroom'] as const
type Filter = (typeof filters)[number]
type Page = 'home' | 'apartments' | 'map' | 'about' | 'detail'
const fmt = (amount: number) => new Intl.NumberFormat('en-KE').format(amount)
const images = [
  'https://images.unsplash.com/photo-1460317442991-0ec209397118?auto=format&fit=crop&w=1000&q=80',
  'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=1000&q=80',
  'https://images.unsplash.com/photo-1600599351175-5c6f4c2fc2b0?auto=format&fit=crop&w=1000&q=80',
]
const GOOGLE_MAPS_LISTING = 'https://www.google.com/maps/place/Kryptons+Apartments+-+Athi+River/@-1.4382467,37.042844,3a,75y,90t/data=!3m8!1e2!3m6!1sCIHM0ogKEICAgICi5duqkQE!2e10!3e12!6shttps:%2F%2Flh3.googleusercontent.com%2Fgrass-cs%2FAABkmLc_loZFr2NfkpgJpdPifkD_nt5o3C9YxWLvRBYi2SMkM4ZGWGVp0GD25pSnTwuUrDEdR3cPvIr8V5gkw2Gkbup1udZuOeagIiMq1bWoslXWoXFZfCXHk1Cksi3gUcXpFbNlaeHl%3Dw114-h86-k-no!7i4608!8i3456!4m7!3m6!1s0x182f7679cc9e8bc7:0x1a4395658e4aaa39!8m2!3d-1.4382467!4d37.042844!10e5!16s%2Fg%2F11fx9pz7sh?entry=ttu'
interface GooglePhoto { name: string; authorAttributions?: { displayName: string; uri?: string }[] }
interface GooglePlacePhotoResponse { places?: { displayName?: { text?: string }; photos?: GooglePhoto[]; editorialSummary?: { text?: string }; rating?: number; userRatingCount?: number }[] }

function markerIcon(active: boolean, campus = false) {
  return divIcon({ className: 'housing-marker-wrap', html: `<span class="housing-marker ${campus ? 'campus-marker' : ''} ${active ? 'marker-active' : ''}">${campus ? '✦' : '<span class="marker-house">⌂</span>'}</span>`, iconSize: [34, 42], iconAnchor: [17, 36], popupAnchor: [0, -34] })
}

function MapMotion({ focus }: { focus: HousingListing | null }) {
  const map = useMap()
  useEffect(() => { if (focus) map.flyTo(latLng(focus.coordinates), focus.id === CAMPUS.id ? 15 : focus.distance?.includes('km') ? 14 : 16, { duration: 0.7 }) }, [focus, map])
  return null
}

function Navbar({ page, navigate, search, setSearch }: { page: Page; navigate: (page: Page) => void; search: string; setSearch: (value: string) => void }) {
  const [open, setOpen] = useState(false)
  const links: { label: string; target: Page }[] = [{ label: 'Home', target: 'home' }, { label: 'Find Accommodation', target: 'apartments' }, { label: 'Map', target: 'map' }, { label: 'About', target: 'about' }]
  return <header className="site-header">
    <button className="site-brand" onClick={() => navigate('home')}><img className="brand-logo" src="/safestay-logo.png" alt=""/><span>Safe<span>Stay</span></span></button>
    <button className="mobile-menu" aria-label="Toggle navigation" aria-expanded={open} onClick={() => setOpen((value) => !value)}>☰</button>
    <nav className={`site-nav ${open ? 'site-nav-open' : ''}`} aria-label="Main navigation">{links.map(({ label, target }) => <button key={target} className={page === target || (page === 'detail' && target === 'apartments') ? 'site-nav-link nav-selected' : 'site-nav-link'} onClick={() => { navigate(target); setOpen(false) }}>{label}</button>)}</nav>
    <div className="header-actions"><label className="header-search"><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search places" aria-label="Search places"/></label><button className="login-button" onClick={() => navigate('about')}>Log in</button><button className="signup-button" onClick={() => navigate('about')}>Sign up</button></div>
  </header>
}

function BuildingImage({ index, large = false, src }: { index: number; large?: boolean; src?: string }) {
  return <div className={`building-image ${large ? 'building-image-large' : ''}`} style={{ backgroundImage: `url(${src ?? images[index % images.length]})` }} role="img" aria-label="Accommodation exterior" />
}

function PropertyCard({ place, onOpen, index = 0, horizontal = false, photoSrc }: { place: HousingListing; onOpen: (place: HousingListing) => void; index?: number; horizontal?: boolean; photoSrc?: string }) {
  return <article className={horizontal ? 'property-card horizontal-card' : 'property-card'}>
    <button className="property-image-button" onClick={() => onOpen(place)} aria-label={`View ${place.name}`}><BuildingImage index={index} src={photoSrc}/><span className="verified-badge">✓ Verified</span></button>
    <div className="property-card-body"><div className="property-card-title-row"><div><span className="property-category">{place.category}</span><button className="property-title" onClick={() => onOpen(place)}>{place.name}</button></div><div className="property-rent"><b>KES {fmt(place.price!.min)}</b>{place.price!.max !== place.price!.min && <span>– {fmt(place.price!.max)}</span>}<small>per month</small></div></div>
      <p className="property-location">⌖ {place.location} · {place.travelTime}</p><div className="property-tags"><span>Wi-Fi</span><span>Water</span><span>Security</span></div><button className="view-details" onClick={() => onOpen(place)}>View details <span>→</span></button>
    </div>
  </article>
}

function PhotoCredit({ photo }: { photo: GooglePhoto }) {
  const author = photo.authorAttributions?.[0]
  if (!author) return null
  const attributionUrl = author.uri?.startsWith('//') ? `https:${author.uri}` : author.uri
  return <span className="photo-credit">Photo: {attributionUrl ? <a href={attributionUrl} target="_blank" rel="noreferrer">{author.displayName}</a> : author.displayName}</span>
}

function App() {
  const [page, setPage] = useState<Page>('home')
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState<Filter>('All')
  const [selected, setSelected] = useState<HousingListing>(HOUSING[0])
  const [focus, setFocus] = useState<HousingListing | null>(CAMPUS)
  const [budget, setBudget] = useState('Any budget')
  const [roomType, setRoomType] = useState('Any room type')
  const [googlePhotos, setGooglePhotos] = useState<GooglePhoto[]>([])
  const [googleDescription, setGoogleDescription] = useState('')
  const [googleRating, setGoogleRating] = useState<{ rating: number; count: number } | null>(null)
  const [photosStatus, setPhotosStatus] = useState<'idle' | 'loading' | 'ready' | 'unavailable'>('idle')
  const googleApiKey = import.meta.env.VITE_GOOGLE_MAPS_API_KEY?.trim()

  useEffect(() => {
    if (!googleApiKey) return
    const controller = new AbortController()
    setPhotosStatus('loading')
    fetch('https://places.googleapis.com/v1/places:searchText', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Goog-Api-Key': googleApiKey, 'X-Goog-FieldMask': 'places.displayName,places.photos,places.editorialSummary,places.rating,places.userRatingCount' },
      body: JSON.stringify({ textQuery: 'Kryptons Apartments Athi River' }),
      signal: controller.signal,
    }).then(async (response) => {
      if (!response.ok) throw new Error('Places API request failed')
      return response.json() as Promise<GooglePlacePhotoResponse>
    }).then((data) => {
      const match = data.places?.find((place) => place.displayName?.text?.toLowerCase().includes('kryptons')) ?? data.places?.[0]
      setGooglePhotos(match?.photos ?? [])
      setGoogleDescription(match?.editorialSummary?.text ?? '')
      setGoogleRating(match?.rating && match.userRatingCount ? { rating: match.rating, count: match.userRatingCount } : null)
      setPhotosStatus(match?.photos?.length ? 'ready' : 'unavailable')
    }).catch(() => { if (!controller.signal.aborted) setPhotosStatus('unavailable') })
    return () => controller.abort()
  }, [googleApiKey])

  const photoUrl = (photo: GooglePhoto, width = 1200) => `https://places.googleapis.com/v1/${photo.name}/media?maxWidthPx=${width}&key=${encodeURIComponent(googleApiKey ?? '')}`

  const visible = useMemo(() => HOUSING.filter((place) => {
    const categoryMatch = filter === 'All' || place.category === filter || (place.id === 'sunset-boulevard' && ['1-Bedroom', '2-Bedroom'].includes(filter))
    const searchMatch = `${place.name} ${place.category} ${place.location}`.toLowerCase().includes(search.toLowerCase())
    const budgetMatch = budget === 'Any budget' || (budget === 'Under KES 8,000' ? place.price!.min < 8000 : budget === 'KES 8,000–15,000' ? place.price!.min >= 8000 && place.price!.min <= 15000 : place.price!.min > 15000)
    const roomMatch = roomType === 'Any room type' || place.category === roomType || (place.id === 'sunset-boulevard' && roomType !== 'Single Rooms' && roomType !== 'Bedsitter')
    return categoryMatch && searchMatch && budgetMatch && roomMatch
  }), [filter, search, budget, roomType])

  const openDetail = (place: HousingListing) => { setSelected(place); setPage('detail'); window.scrollTo({ top: 0, behavior: 'smooth' }) }
  const browse = () => { setFilter(roomType === 'Any room type' ? 'All' : roomType as Filter); setPage('apartments'); window.scrollTo({ top: 0, behavior: 'smooth' }) }

  return <div className="site-shell">
    <Navbar page={page} navigate={(next) => { setPage(next); window.scrollTo({ top: 0, behavior: 'smooth' }) }} search={search} setSearch={setSearch}/>
    {page === 'home' && <main>
      <section className="home-hero"><div className="hero-content"><span className="hero-kicker">YOUR NEXT CHAPTER STARTS HERE</span><h1>Find Your Ideal<br/>Student <em>Home</em></h1><p>Verified private hostels and rentals around Daystar University, Athi River</p>
        <form className="hero-search" onSubmit={(event) => { event.preventDefault(); browse() }}><label><span>⌖</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Location / Area" aria-label="Location or area"/></label><label><span className="search-label">Budget</span><select value={budget} onChange={(event) => setBudget(event.target.value)}><option>Any budget</option><option>Under KES 8,000</option><option>KES 8,000–15,000</option><option>Over KES 15,000</option></select></label><label><span className="search-label">Room type</span><select value={roomType} onChange={(event) => setRoomType(event.target.value)}><option>Any room type</option>{filters.slice(1).map((option) => <option key={option}>{option}</option>)}</select></label><button type="submit">Search</button></form>
      </div></section>
      <section className="featured-section"><div className="section-heading"><div><span className="section-kicker">A PLACE TO CALL YOUR OWN</span><h2>Featured accommodation</h2></div><button className="text-link" onClick={() => setPage('apartments')}>View all <span>→</span></button></div><div className="featured-grid">{HOUSING.slice(0, 3).map((place, index) => <PropertyCard key={place.id} place={place} index={index} onOpen={openDetail} photoSrc={place.id === 'kryptons-apt' && googlePhotos[0] ? photoUrl(googlePhotos[0], 800) : undefined}/>)}</div></section>
    </main>}

    {page === 'apartments' && <main className="listings-page"><div className="page-title"><span className="section-kicker">DAYSTAR UNIVERSITY · ATHI RIVER</span><h1>Find Accommodation</h1><p>Private hostels and rentals around Daystar University, Athi River</p></div><form className="listing-search" onSubmit={(event) => event.preventDefault()}><span>⌕</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by name or area…" aria-label="Search by name or area"/><button type="submit">Search</button></form><div className="listing-filter-row"><div className="listing-filters" role="tablist" aria-label="Filter by room type">{filters.map((option) => <button role="tab" aria-selected={filter === option} className={filter === option ? 'filter-chip filter-chip-active' : 'filter-chip'} key={option} onClick={() => setFilter(option)}>{option === 'All' ? 'All stays' : option}</button>)}</div><span className="result-count">Showing <b>{visible.length}</b> results</span></div><div className="listing-cards">{visible.map((place, index) => <PropertyCard key={place.id} place={place} index={index} horizontal onOpen={openDetail} photoSrc={place.id === 'kryptons-apt' && googlePhotos[0] ? photoUrl(googlePhotos[0], 800) : undefined}/>)}</div>{visible.length === 0 && <div className="no-results">No stays match those filters. Try a different search.</div>}</main>}

    {page === 'detail' && <main className="detail-page"><div className="breadcrumbs"><button onClick={() => setPage('apartments')}>Find Accommodation</button><span>›</span><span>{selected.name}</span></div>
      {selected.id === 'kryptons-apt' && googlePhotos.length > 0 ? <div className="google-photo-gallery"><div className="google-photo-main"><img src={photoUrl(googlePhotos[0])} alt={`${selected.name} photo 1`}/><PhotoCredit photo={googlePhotos[0]}/></div><div className="google-photo-thumbs">{googlePhotos.slice(1).map((photo, index) => <div className="google-photo-thumb" key={photo.name}><img src={photoUrl(photo, 600)} alt={`${selected.name} photo ${index + 2}`}/><PhotoCredit photo={photo}/></div>)}</div><a className="google-photos-link" href={GOOGLE_MAPS_LISTING} target="_blank" rel="noreferrer">See all 11 photos on Google Maps ↗</a></div> : <><div className="detail-gallery"><BuildingImage index={HOUSING.indexOf(selected)} large/><div className="gallery-side"><BuildingImage index={1}/><BuildingImage index={2}/></div></div>{selected.id === 'kryptons-apt' && <div className="photo-api-note">{photosStatus === 'loading' ? 'Loading property photos…' : photosStatus === 'unavailable' && googleApiKey ? 'Photos could not be loaded. Check the Places API key and billing.' : 'Add a Google Places API key to show the listing photos here.'} <a href={GOOGLE_MAPS_LISTING} target="_blank" rel="noreferrer">View all 11 photos on Google Maps ↗</a></div>}</>}
      <div className="detail-layout"><section className="detail-description"><span className="section-kicker">VERIFIED ACCOMMODATION</span><h1>{selected.name}</h1><p className="detail-location">⌖ {selected.location} · {selected.distance} from campus · {selected.travelTime}</p><div className="verification-line"><span>✓ Verified listing</span>{googleRating && selected.id === 'kryptons-apt' && <span>★ {googleRating.rating.toFixed(1)} Google · {googleRating.count} ratings</span>}</div><p className="detail-copy">{googleDescription || (selected.id === 'kryptons-apt' ? 'Student-friendly self-contained studios near Daystar, with private balconies, granite-top kitchenettes, and ensuite bathrooms with hot water.' : 'A comfortable, student-friendly place to call home near Daystar University. Enjoy convenient access to campus and the essentials for everyday living.')}</p><h2>Facilities & features</h2><div className="feature-grid">{(selected.features ?? []).map((feature) => <span key={feature}><i>✓</i>{feature}</span>)}<span><i>◉</i> Wi-Fi</span><span><i>♧</i> Water</span><span><i>◈</i> Security</span></div><div className="review-box"><b>Verified stay</b><span>Listing reviewed for accuracy by SafeStay.</span></div></section><aside className="booking-card"><div className="booking-price"><b>KES {fmt(selected.price!.min)}{selected.price!.min !== selected.price!.max && `–${fmt(selected.price!.max)}`}</b><span> / month</span></div><p>{selected.category} · Available now</p><button className="request-button" onClick={(event) => { event.currentTarget.textContent = 'Viewing request sent ✓' }}>Request viewing</button><button className="contact-button" onClick={(event) => { event.currentTarget.textContent = 'Provider contacted ✓' }}>Contact provider</button><small>Listed by a verified landlord</small></aside></div></main>}

    {page === 'map' && <main className="map-page"><div className="map-page-heading"><div><span className="section-kicker">ATHI RIVER CAMPUS</span><h1>Accommodation <em>map</em></h1><p>Explore verified student stays around Daystar University.</p></div><span className="map-count"><i/> LIVE MAP · {visible.length} places</span></div><div className="map-page-filters">{filters.map((option) => <button className={filter === option ? 'map-filter-active' : ''} key={option} onClick={() => setFilter(option)}>{option === 'All' ? 'All places' : option}</button>)}</div><section className="map-split grid min-h-[475px] max-h-[780px] grid-cols-[minmax(330px,39%)_1fr] overflow-hidden rounded-md border border-zinc-700 bg-zinc-900 shadow-2xl"><aside className="map-list-panel"><div className="map-list-heading"><div><b>Nearby stays</b><small>✓ Verified accommodation</small></div><button onClick={() => setFocus(CAMPUS)}>⌖ Campus</button></div><div className="map-list-scroll">{visible.map((place) => <button className={`map-stay ${focus?.id === place.id ? 'map-stay-active' : ''}`} key={place.id} onMouseEnter={() => setFocus(place)} onClick={() => setFocus(place)}><span className="map-stay-icon">⌂</span><span className="map-stay-name"><b>{place.name}</b><small>{place.category} · {place.distance} · {place.travelTime}</small></span><span className="map-stay-price"><b>KSh {fmt(place.price!.min)}</b><small>/month</small></span></button>)}</div></aside><div className="map-frame relative min-w-0 bg-zinc-900"><MapContainer center={CAMPUS.coordinates} zoom={14} scrollWheelZoom className="leaflet-map" zoomControl={false}><TileLayer attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors' url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/><MapMotion focus={focus}/><Marker position={CAMPUS.coordinates} icon={markerIcon(focus?.id === CAMPUS.id, true)} eventHandlers={{ click: () => setFocus(CAMPUS) }}><Popup><strong>Daystar Main Campus Gate</strong><br/>Athi River Campus</Popup></Marker>{visible.map((place) => <Marker key={place.id} position={place.coordinates} icon={markerIcon(focus?.id === place.id)} eventHandlers={{ click: () => setFocus(place), mouseover: () => setFocus(place) }}><Popup><strong>{place.name}</strong><br/>{place.category} · KSh {fmt(place.price!.min)}–{fmt(place.price!.max)} / month<br/>{place.distance} · {place.travelTime}</Popup></Marker>)}</MapContainer><div className="map-overlay-label"><span className="campus-pulse"/> DAYSTAR MAIN GATE <i/> ATHI RIVER</div></div></section></main>}

    {page === 'about' && <main className="about-page"><span className="section-kicker">ABOUT DAYSTAR UNIVERSITY</span><h1>A campus community<br/>in <em>Athi River.</em></h1><p>Find a comfortable place to live while you learn, grow, and make the most of campus life. SafeStay brings nearby student accommodation into one easy-to-explore guide.</p><button className="request-button" onClick={() => setPage('apartments')}>Browse accommodation →</button><button className="about-map-link" onClick={() => setPage('map')}>Explore the map</button></main>}

    <footer className="site-footer"><button className="footer-brand" onClick={() => setPage('home')}>⌂ SafeStay</button><div><button onClick={() => setPage('about')}>About</button><button onClick={() => setPage('apartments')}>Find accommodation</button><button onClick={() => setPage('map')}>Map</button></div><span>Made for your campus life · Athi River, Kenya</span></footer>
  </div>
}

export default App
