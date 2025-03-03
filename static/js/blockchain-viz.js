import * as THREE from 'https://unpkg.com/three@0.157.0/build/three.module.js';
import { EffectComposer } from 'https://unpkg.com/three@0.157.0/examples/jsm/postprocessing/EffectComposer.js';
import { RenderPass } from 'https://unpkg.com/three@0.157.0/examples/jsm/postprocessing/RenderPass.js';
import { UnrealBloomPass } from 'https://unpkg.com/three@0.157.0/examples/jsm/postprocessing/UnrealBloomPass.js';

class BlockchainViz {
    constructor(container) {
        if (!container) {
            console.error('No container provided for BlockchainViz');
            return;
        }
        this.container = container;
        this.prophecies = [];
        this.particles = [];
        this.isMinimalView = false;

        this.init();
        this.createParticles();
        this.animate();

        // Add toggle button
        this.createToggleButton();

        console.log('BlockchainViz initialized');
    }

    createToggleButton() {
        const button = document.createElement('button');
        button.className = 'viz-toggle';
        button.textContent = 'Toggle Minimal View';
        button.onclick = () => this.toggleView();
        this.container.appendChild(button);
    }

    toggleView() {
        this.isMinimalView = !this.isMinimalView;

        if (this.particleSystem) {
            // Adjust particle visibility and size
            this.particleSystem.material.size = this.isMinimalView ? 1 : 2;
            this.particleSystem.material.opacity = this.isMinimalView ? 0.3 : 0.5;
        }

        // Adjust prophecy spheres
        this.prophecies.forEach(prophecy => {
            prophecy.mesh.material.opacity = this.isMinimalView ? 0.4 : 0.7;
            prophecy.mesh.scale.setScalar(this.isMinimalView ? 0.75 : 1);
        });

        // Adjust bloom effect
        if (this.bloomPass) {
            this.bloomPass.strength = this.isMinimalView ? 0.5 : 1.0;
            this.bloomPass.radius = this.isMinimalView ? 0.2 : 0.3;
        }
    }

    init() {
        try {
            // Scene setup with darker background for subtlety
            this.scene = new THREE.Scene();
            this.scene.background = new THREE.Color(0x050510);

            // Camera setup
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 2000);
            this.camera.position.z = 100;

            // Renderer setup
            this.renderer = new THREE.WebGLRenderer({ 
                antialias: true,
                alpha: true,
                powerPreference: "high-performance"
            });
            this.renderer.setPixelRatio(window.devicePixelRatio);
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.container.appendChild(this.renderer.domElement);

            // Minimal lighting
            const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
            const pointLight = new THREE.PointLight(0x4a90e2, 0.8);
            pointLight.position.set(0, 0, 50);
            this.scene.add(ambientLight, pointLight);

            // Subtle bloom effect
            this.composer = new EffectComposer(this.renderer);
            const renderPass = new RenderPass(this.scene, this.camera);
            this.bloomPass = new UnrealBloomPass(
                new THREE.Vector2(window.innerWidth, window.innerHeight),
                1.0,
                0.3,
                0.7
            );
            this.composer.addPass(renderPass);
            this.composer.addPass(this.bloomPass);

            window.addEventListener('resize', this.onWindowResize.bind(this));

        } catch (error) {
            console.error('Error initializing Three.js scene:', error);
        }
    }

    createParticles() {
        try {
            const geometry = new THREE.BufferGeometry();
            const vertices = [];
            const colors = [];

            // Reduced number of particles
            const particleCount = this.isMinimalView ? 1500 : 3000;
            const spread = this.isMinimalView ? 600 : 800;

            for (let i = 0; i < particleCount; i++) {
                vertices.push(
                    THREE.MathUtils.randFloatSpread(spread),
                    THREE.MathUtils.randFloatSpread(spread),
                    THREE.MathUtils.randFloatSpread(spread)
                );

                const color = new THREE.Color();
                color.setHSL(Math.random(), 0.3, 0.5); // More subtle colors
                colors.push(color.r, color.g, color.b);
            }

            geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
            geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

            const material = new THREE.PointsMaterial({
                size: this.isMinimalView ? 1 : 2,
                vertexColors: true,
                transparent: true,
                opacity: this.isMinimalView ? 0.3 : 0.5,
                sizeAttenuation: true
            });

            this.particleSystem = new THREE.Points(geometry, material);
            this.scene.add(this.particleSystem);

        } catch (error) {
            console.error('Error creating particle system:', error);
        }
    }

    addProphecy(prophecyData) {
        try {
            const geometry = new THREE.SphereGeometry(1.5, 16, 16); // Reduced geometry complexity
            const material = new THREE.MeshPhongMaterial({
                color: 0x4a90e2,
                emissive: 0x4a90e2,
                emissiveIntensity: 0.2,
                transparent: true,
                opacity: this.isMinimalView ? 0.4 : 0.7,
                shininess: 20
            });

            const sphere = new THREE.Mesh(geometry, material);

            const timestamp = new Date(prophecyData.created_at).getTime();
            const radius = this.isMinimalView ? 30 : 40;
            sphere.position.x = Math.sin(timestamp) * radius;
            sphere.position.y = Math.cos(timestamp) * radius;
            sphere.position.z = Math.sin(timestamp * 0.5) * radius;

            this.prophecies.push({
                mesh: sphere,
                timestamp: timestamp
            });

            this.scene.add(sphere);

        } catch (error) {
            console.error('Error adding prophecy:', error);
        }
    }

    animate() {
        try {
            requestAnimationFrame(this.animate.bind(this));

            // Minimal rotation for particle system
            if (this.particleSystem) {
                this.particleSystem.rotation.x += 0.0001;
                this.particleSystem.rotation.y += 0.0001;
            }

            // Subtle prophecy sphere animation
            this.prophecies.forEach(prophecy => {
                prophecy.mesh.rotation.y += 0.005;
                if (!this.isMinimalView) {
                    const time = Date.now() * 0.0003;
                    prophecy.mesh.position.y += Math.sin(time) * 0.01;
                }
            });

            this.composer.render();

        } catch (error) {
            console.error('Error in animation loop:', error);
        }
    }

    onWindowResize() {
        try {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
            this.composer.setSize(window.innerWidth, window.innerHeight);
        } catch (error) {
            console.error('Error handling window resize:', error);
        }
    }
}

export default BlockchainViz;